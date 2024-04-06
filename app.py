from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
import random
app = Flask(__name__)

# Sample thesaurus data
thesaurus_data = {
    "graceful": {
        "definition": "having or showing grace or elegance",
        "synonyms": ["elegant", "graceful", "refined"],
        "antonyms": ["awkward", "clumsy", "ungainly"]
    },
    "elegant": {
        "definition": "pleasingly graceful and stylish",
        "synonyms": ["graceful", "refined", "sophisticated"],
        "antonyms": ["awkward", "clumsy", "ungainly"]
    },
    "refined": {
        "definition": "elegant and cultured in appearance, manner, or taste",
        "synonyms": ["sophisticated", "elegant", "cultured"],
        "antonyms": ["uncultured", "unsophisticated", "crude"]
    },
    "awkward": {
        "definition": "causing difficulty; hard to do or deal with",
        "synonyms": ["clumsy", "uncoordinated", "inept"],
        "antonyms": ["graceful", "elegant", "refined"]
    },
    "clumsy": {
        "definition": "awkward in movement or in handling things",
        "synonyms": ["awkward", "uncoordinated", "bungling"],
        "antonyms": ["graceful", "elegant", "refined"]
    },
    "ungainly": {
        "definition": "lacking grace in movement or appearance",
        "synonyms": ["awkward", "clumsy", "ungraceful"],
        "antonyms": ["graceful", "elegant", "refined"]
    },
    "sophisticated": {
        "definition": "having acquired worldly knowledge or refinement; cultured",
        "synonyms": ["refined", "elegant", "urbane"],
        "antonyms": ["uncultured", "unsophisticated", "crude"]
    },
    "cultured": {
        "definition": "characterized by refined taste and manners",
        "synonyms": ["refined", "sophisticated", "civilized"],
        "antonyms": ["uncultured", "unsophisticated", "crude"]
    },
    "uncoordinated": {
        "definition": "not properly planned or regulated",
        "synonyms": ["awkward", "clumsy", "inept"],
        "antonyms": ["coordinated", "graceful", "elegant"]
    },
    "inept": {
        "definition": "having or showing no skill; clumsy",
        "synonyms": ["awkward", "clumsy", "incompetent"],
        "antonyms": ["skilled", "competent", "proficient"]
    },
    "bungling": {
        "definition": "to act or work clumsily and awkwardly",
        "synonyms": ["awkward", "clumsy", "inept"],
        "antonyms": ["skilled", "competent", "proficient"]
    },
    "ungraceful": {
        "definition": "lacking grace or elegance",
        "synonyms": ["awkward", "clumsy", "ungainly"],
        "antonyms": ["graceful", "elegant", "refined"]
    },
    "urbane": {
        "definition": "suave, courteous, and refined in manner",
        "synonyms": ["sophisticated", "cultured", "polished"],
        "antonyms": ["uncouth", "unsophisticated", "crude"]
    },
    "civilized": {
        "definition": "having an advanced or humane culture, society, etc.",
        "synonyms": ["cultured", "refined", "sophisticated"],
        "antonyms": ["uncivilized", "primitive", "barbaric"]
    },
    "incompetent": {
        "definition": "not having or showing the necessary skills to do something successfully",
        "synonyms": ["inept", "unskilled", "inadequate"],
        "antonyms": ["competent", "skilled", "proficient"]
    },
    "skilled": {
        "definition": "having the ability to do something well",
        "synonyms": ["competent", "proficient", "adept"],
        "antonyms": ["inept", "incompetent", "unskilled"]
    },
    "competent": {
        "definition": "having the necessary ability, knowledge, or skill to do something successfully",
        "synonyms": ["skilled", "proficient", "capable"],
        "antonyms": ["incompetent", "inept", "unskilled"]
    },
    "proficient": {
        "definition": "competent or skilled in doing or using something",
        "synonyms": ["skilled", "competent", "adept"],
        "antonyms": ["inept", "incompetent", "unskilled"]
    },
    "polished": {
        "definition": "showing a high degree of refinement and the assurance that comes from wide social experience",
        "synonyms": ["urbane", "sophisticated", "cultured"],
        "antonyms": ["uncouth", "unsophisticated", "crude"]
    },
    "uncouth": {
        "definition": "lacking good manners, refinement, or grace",
        "synonyms": ["rude", "unrefined", "uncultivated"],
        "antonyms": ["urbane", "sophisticated", "cultured"]
    },
    "primitive": {
        "definition": "relating to, denoting, or preserving the character of an early stage in the evolutionary or historical development of something",
        "synonyms": ["uncivilized", "barbaric", "savage"],
        "antonyms": ["civilized", "refined", "sophisticated"]
    },
    "barbaric": {
        "definition": "savagely cruel; exceedingly brutal",
        "synonyms": ["uncivilized", "primitive", "savage"],
        "antonyms": ["civilized", "refined", "sophisticated"]
    },
    "uncivilized": {
        "definition": "not civilized or cultured; primitive",
        "synonyms": ["barbaric", "primitive", "savage"],
        "antonyms": ["civilized", "refined", "sophisticated"]
    },
    "rude": {
        "definition": "offensively impolite or ill-mannered",
        "synonyms": ["uncouth", "crude", "impolite"],
        "antonyms": ["polite", "courteous", "well-mannered"]
    },
    "unrefined": {
        "definition": "not refined, purified, or processed",
        "synonyms": ["uncouth", "crude", "unpolished"],
        "antonyms": ["polished", "sophisticated", "refined"]
    },
    "uncultivated": {
        "definition": "not improved by cultivation or development",
        "synonyms": ["crude", "unrefined", "undeveloped"],
        "antonyms": ["cultivated", "refined", "sophisticated"]
    },
    "savage": {
        "definition": "fierce, violent, and uncontrolled",
        "synonyms": ["primitive", "barbaric", "uncivilized"],
        "antonyms": ["civilized", "refined", "sophisticated"]
    },
    "impolite": {
        "definition": "not having or showing good manners; rude",
        "synonyms": ["rude", "uncouth", "crude"],
        "antonyms": ["polite", "courteous", "well-mannered"]
    },
    "unpolished": {
        "definition": "not shiny or glossy",
        "synonyms": ["crude", "unrefined", "rough"],
        "antonyms": ["polished", "refined", "sophisticated"]
    },
    "undeveloped": {
        "definition": "not yet fully formed, grown, or matured",
        "synonyms": ["crude", "unrefined", "immature"],
        "antonyms": ["developed", "mature", "grown"]
    },
    "rough": {
        "definition": "having an uneven or irregular surface",
        "synonyms": ["unpolished", "coarse", "ragged"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    "immature": {
        "definition": "not fully developed or grown",
        "synonyms": ["undeveloped", "juvenile", "unripe"],
        "antonyms": ["mature", "grown", "developed"]
    },
    "coarse": {
        "definition": "rough or loose in texture or grain",
        "synonyms": ["rough", "unpolished", "gritty"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    "juvenile": {
        "definition": "of, for, or relating to young people",
        "synonyms": ["immature", "youthful", "adolescent"],
        "antonyms": ["mature", "adult", "grown-up"]
    },
    "unripe": {
        "definition": "not fully matured",
        "synonyms": ["immature", "green", "unseasoned"],
        "antonyms": ["ripe", "mature", "ready"]
    },
    "gritty": {
        "definition": "containing or covered with grit",
        "synonyms": ["coarse", "rough", "gravelly"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    "youthful": {
        "definition": "having the appearance, freshness, vigor, or other qualities of youth",
        "synonyms": ["juvenile", "adolescent", "young"],
        "antonyms": ["mature", "adult", "grown-up"]
    },
    "adolescent": {
        "definition": "relating to or denoting a young person in the process of developing from a child into an adult",
        "synonyms": ["juvenile", "youthful", "teenage"],
        "antonyms": ["mature", "adult", "grown-up"]
    },
    "green": {
        "definition": "of the color between blue and yellow in the spectrum",
        "synonyms": ["unripe", "immature", "unseasoned"],
        "antonyms": ["ripe", "mature", "ready"]
    },
    "unseasoned": {
        "definition": "not mature or fully developed",
        "synonyms": ["immature", "unripe", "green"],
        "antonyms": ["ripe", "mature", "ready"]
    },
    "gravelly": {
        "definition": "covered with gravel",
        "synonyms": ["gritty", "sandy", "pebbly"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    "teenage": {
        "definition": "relating to or characteristic of teenagers",
        "synonyms": ["adolescent", "youthful", "young"],
        "antonyms": ["mature", "adult", "grown-up"]
    },
    "sandy": {
        "definition": "covered with or consisting mostly of sand",
        "synonyms": ["gravelly", "gritty", "pebbly"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    "pebbly": {
        "definition": "covered with or full of small, rounded stones",
        "synonyms": ["gravelly", "sandy", "gritty"],
        "antonyms": ["smooth", "polished", "refined"]
    },
    # Add more words in a similar format
}


def generate_graph(word, word_info):
  synonyms = word_info.get('synonyms', [])
  if not synonyms:
    return None  # Return None if there are no synonyms

  G = nx.Graph()
  G.add_node(word, label=word)  # Add the search word as the central node

  for synonym in synonyms:
    G.add_node(synonym, label=synonym)  # Add nodes for each synonym
    G.add_edge(word, synonym)  # Connect search word to its synonyms

  # Create a plot and draw the graph
  fig, ax = plt.subplots(figsize=(8, 6))
  pos = nx.spring_layout(G, seed=42)
  nx.draw(G,
          pos=pos,
          ax=ax,
          with_labels=True,
          node_color='skyblue',
          node_size=2000,
          font_size=10,
          font_weight='bold',
          edge_color='gray')
  ax.set_title('Synonyms Graph of ' + word)
  ax.set_axis_off()
  plt.tight_layout()

  # Convert plot to HTML using mpld3
  graph_html = mpld3.fig_to_html(fig)
  plt.close()

  return graph_html


@app.route('/', methods=['GET', 'POST'])
def index():
    default_word = "graceful"  # Change this to the default word you want to set

    # Randomly select a word from the thesaurus data
    random_word = random.choice(list(thesaurus_data.keys()))

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').lower()
        word_info = thesaurus_data.get(search_term, {'synonyms': []})

        if word_info['synonyms']:
            graph_html = generate_graph(search_term, word_info)
            if graph_html:
                return render_template('index.html',
                                       word=search_term,
                                       word_info=word_info,
                                       graph_html=graph_html)
            else:
                return render_template('not_found.html', word=search_term)
        else:
            return render_template('not_found.html', word=search_term)

    # If no search term is provided in the request or if it's a GET request,
    # display information for the default word
    word_info = thesaurus_data.get(default_word, {'synonyms': []})
    graph_html = generate_graph(default_word, word_info)
    return render_template('index.html', word=default_word, word_info=word_info, graph_html=graph_html, random_word=random_word)

if __name__ == '__main__':
  app.run()
