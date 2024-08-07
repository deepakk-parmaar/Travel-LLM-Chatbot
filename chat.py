import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model import chat_groq, chatOllama
from flight_utils import search_flights,search_hotel

def get_city_code(query):
    """
    Get the city code.
    """
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        User has provided a query retrive information from that.
        Return the output in the following format only:
        {{
            "source" : "source IATA code",
            "destination" : "destination IATA code",
            "date" : "yyyy-mm-dd",
            "adults" : number of adults, default 1
        }} 
        <|eot_id|><|start_header_id|>user<|end_header_id>
        Get the city IATA code for the given city name {query}.
        <|eot_id|><|start_header_id|>assistant<|end_header_id>
        """, input_variables=["query"]
    )
    model = chat_groq()
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"query": query})
    # print(response)
    return response

async def flight_query(content: str, message_placeholder):
    """
    Stream a chat from Llama using the AsyncClient.
    """
    model = chat_groq()
    message_placeholder.text("Getting City Codes...")
    cities = get_city_code(content)
    cities = json.loads(cities)
    print(cities)
    message_placeholder.text("Getting Flights...")
    flights = search_flights(cities['source'], cities['destination'],cities['date'],cities['adults'])
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are system to help user queries regarding flight booking.
        Given Flight details {flights}
        <|eot_id|><|start_header_id|>user<|end_header_id>
        Here is the user question: {question}
        <|eot_id|><|start_header_id|>assistant<|end_header_id>
        """, input_variables=["flights","question"]
    )
    rag_chain = prompt| model| StrOutputParser()
    message_placeholder.text("Generating Response...")
    response = ""
    async for part in rag_chain.astream(input={"flights":flights,"question":content}):
        response += part
        message_placeholder.markdown(response)
    return response

def city_code(query: str):
    """
    Get the city code.
    """
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        User has provided a query retrive information from that.
        Return City IATA code in one word only
        <|eot_id|><|start_header_id|>user<|end_header_id>
        Get the city IATA code for the given city name {query}.
        <|eot_id|><|start_header_id|>assistant<|end_header_id>
        """, input_variables=["query"]
    )
    model = chat_groq()
    chain = prompt | model | StrOutputParser()
    response = chain.invoke({"query": query})
    # print(response)
    return response

async def hotel_query(content: str, message_placeholder):
    """
    Stream a chat from Llama using the AsyncClient.
    """
    model = chat_groq()
    message_placeholder.text("Getting City Codes...")
    city = city_code(content)
    message_placeholder.text("Getting Hotels...")
    hotels,hotel_map = search_hotel(city)
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are system to help user queries regarding hotel booking.
        Given Hotel details {hotels}
        <|eot_id|><|start_header_id|>user<|end_header_id>
        Here is the user question: {question}
        <|eot_id|><|start_header_id|>assistant<|end_header_id>
        """, input_variables=["hotels","question"]
    )
    rag_chain = prompt| model| StrOutputParser()
    message_placeholder.text("Generating Response...")
    response = ""
    async for part in rag_chain.astream(input={"hotels":hotels,"question":content}):
        response += part
        message_placeholder.markdown(response)
    return response,hotel_map

def get_route(query):
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        Given the user question below, classify it as either
        being about `flight` or `hotel` else return None
        Do not respond with more than one word.
        <|eot_id|><|start_header_id|>user<|end_header_id>
        Here is the user query : {query}
        <|eot_id|><|start_header_id|>assistant<|end_header_id>
        """, input_variables=["query"]
    )
    model = chat_groq()
    chain = prompt | model | StrOutputParser()
    route = chain.invoke({"query": query})
    return route

if __name__ == "__main__":
    response = city_code('give hotels in mumbai')
    # book_Flights('New York', 'Los Angeles', '2022-12-01')