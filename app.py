from scholarly import scholarly
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import spacy

app = FastAPI()


nlp = spacy.load("en_core_web_sm")

def get_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if token.is_stop == False and token.is_punct == False]
    
    return " ".join(keywords)
     
# Research Paper Fetching
def get_research_papers(query):
  search_query = scholarly.search_pubs(query)
  num_papers = 10
  papers = []
  for i, paper in enumerate(search_query):
      if i >= num_papers:
          break
      papers.append({
          "title": paper['bib']['title'],
          "author": paper['bib'].get('author', 'Unknown'),
          "link": paper.get('pub_url', 'N/A'),
          "pdf_Link": paper.get('eprint_url', 'N/A'),
        

      })

  print(papers)
  return list(papers)

# define query model
class QueryRequest(BaseModel):
    text: str

# Endpoint: Get Research Papers
@app.post("/research_papers")
async def fetch_research_papers(request: QueryRequest):
    keywords = get_keywords(request.text)
    papers_list = get_research_papers(keywords)
    return {"papers": papers_list, "keywords": keywords}



# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)