from typing import List

from snowflake.snowpark.session import Session
from snowflake.core import Root
from snowflake.cortex import Complete

import streamlit as st

from trulens.core import TruSession
from trulens.core.guardrails.base import context_filter
from trulens.apps.custom import TruCustomApp
from trulens.apps.custom import instrument
from trulens.providers.cortex import Cortex
from trulens.core import Feedback
from trulens.core import Select
import numpy as np

from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import snowflake.connector

import json
import logging
logger = logging.getLogger(__name__)

connection_details = {
  "account":  st.secrets["SNOWFLAKE_ACCOUNT"],
  "user": st.secrets["SNOWFLAKE_USER"],
  "password": st.secrets["SNOWFLAKE_USER_PASSWORD"],
  "role": st.secrets["SNOWFLAKE_ROLE"],
  "database": st.secrets["SNOWFLAKE_DATABASE"],
  "schema": st.secrets["SNOWFLAKE_SCHEMA"],
  "warehouse": st.secrets["SNOWFLAKE_WAREHOUSE"]
}

engine = create_engine(URL(
    account=st.secrets["SNOWFLAKE_ACCOUNT"],
    warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
    database=st.secrets["SNOWFLAKE_DATABASE"],
    schema=st.secrets["SNOWFLAKE_SCHEMA"],
    user=st.secrets["SNOWFLAKE_USER"],
    password=st.secrets["SNOWFLAKE_USER_PASSWORD"],
    ),
)

snowflake_connection = snowflake.connector.connect(**connection_details)
"""
tru = TruSession(database_engine = engine)
"""
session = Session.builder.configs(connection_details).create()

class CortexSearchRetriever:

    def __init__(self, snowpark_session: Session, limit_to_retrieve: int = 4):
        self._snowpark_session = snowpark_session
        self._limit_to_retrieve = limit_to_retrieve

    def retrieve(self, query: str) -> List[str]:
        root = Root(self._snowpark_session)
        cortex_search_service = (
        root
        .databases[st.secrets["SNOWFLAKE_DATABASE"]]
        .schemas[st.secrets["SNOWFLAKE_SCHEMA"]]
        .cortex_search_services[st.secrets["SNOWFLAKE_CORTEX_SEARCH_SERVICE"]]
    )
        resp = cortex_search_service.search(
                query=query,
                columns=["SUMMARY"],
                limit=self._limit_to_retrieve,
            )

        if resp.results:
            return [curr["SUMMARY"] for curr in resp.results]
        else:
            return []
        
model_name = st.session_state.get("model_name", "mistral-large2")
provider = Cortex(session, model_engine=model_name)

f_groundedness = (
    Feedback(
    provider.groundedness_measure_with_cot_reasons, name="Groundedness")
    .on(Select.RecordCalls.retrieve_context.rets[:].collect())
    .on_output()
)

f_context_relevance = (
    Feedback(
    provider.context_relevance,
    name="Context Relevance")
    .on_input()
    .on(Select.RecordCalls.retrieve_context.rets[:])
    .aggregate(np.mean)
)

f_answer_relevance = (
    Feedback(
    provider.relevance,
    name="Answer Relevance")
    .on_input()
    .on_output()
    .aggregate(np.mean)
)

feedbacks = [f_context_relevance,
            f_answer_relevance,
            f_groundedness,
        ]

class RAG:

  def __init__(self):
    self.retriever = CortexSearchRetriever(snowpark_session=session, limit_to_retrieve=4)

  @instrument
  def retrieve_context(self, query: str) -> list:
    """
    Retrieve relevant text from vector store.
    """
    return self.retriever.retrieve(query)

  @instrument
  def generate_completion(self, query: str, context_str: list) -> str:
    """
    Generate answer from context.
    """
    prompt = f"""
    [INST]
    You are an expert chat assistance that extracs information from the CONTEXT provided
    between <context> and </context> tags.
    When ansering the question contained between <question> and </question> tags
    be concise and do not hallucinate. 
    If you don´t have the information just say so.
    Only anwer the question if you can extract it from the CONTEXT provideed.
           
    Do not mention the CONTEXT used in your answer.

    <context>          
    {context_str}
    </context>
    <question>  
    {query}
    </question>
    [/INST]
    Answer:
    """
 

    df_response = None
    print(f"************************************")

    prompt = prompt.format(context_str=context_str, query=query)
    print(f"{prompt}")
    print(f"====================================")
    return Complete(st.session_state.model_name, prompt)
    """
    df_response = session.sql("select snowflake.cortex.complete(?, ?) as response", params=[st.session_state.model_name, prompt]).collect()
    """

  @instrument
  def query(self, query: str) -> str:
    context_str = self.retrieve_context(query)
    return self.generate_completion(query, context_str)

class filtered_RAG(RAG):

    @instrument
    @context_filter(f_context_relevance, 0.75, keyword_for_prompt="query")
    def retrieve_context(self, query: str) -> list:
        """
        Retrieve relevant text from vector store.
        """
        results = self.retriever.retrieve(query)
        return results
    
rag = RAG()


tru_rag = TruCustomApp(rag,
    app_version = 'v1',
    app_name = 'RAG',
    feedbacks = feedbacks)

filtered_rag = filtered_RAG()

filtered_tru_rag = TruCustomApp(filtered_rag,
    app_version = 'v2',
    app_name = 'RAG',
    feedbacks = feedbacks)
