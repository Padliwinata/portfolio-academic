from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud(concepts):
    text = ' '.join(concepts)
    wc = WordCloud(width=800, height=400).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    return fig
