from rouge import Rouge
import gensim.downloader as api
from nltk.corpus import stopwords
from nltk import download
from gensim.corpora import Dictionary
from gensim.similarities import SparseTermSimilarityMatrix, WordEmbeddingSimilarityIndex

import csv


class TitleSimilarity:
    def __int__(self):
        download('stopwords')
        self.stop_words = stopwords.words('english')
        self.w2v_model = api.load("glove-wiki-gigaword-50")

    def scores_rouge_1_f(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-1']['f']

    def scores_rouge_1_p(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-1']['p']

    def scores_rouge_1_r(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-1']['r']

    def scores_rouge_2_f(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-2']['f']

    def scores_rouge_2_p(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-2']['p']

    def scores_rouge_2_r(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-2']['r']

    def scores_rouge_l_f(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-l']['f']

    def scores_rouge_l_p(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-l']['p']

    def scores_rouge_l_r(self, model_out, reference):
        rouge = Rouge()
        scores = rouge.get_scores(model_out, reference, avg=True)

        return scores['rouge-l']['r']

    def scores_scm(self, model_out, reference):
        model_out = model_out.lower().split()
        reference = reference.lower().split()

        model_out = [w for w in model_out if w not in self.stop_words]
        reference = [w for w in reference if w not in self.stop_words]

        documents = [model_out, reference]
        dictionary = Dictionary(documents)

        model_out = dictionary.doc2bow(model_out)
        reference = dictionary.doc2bow(reference)

        similarity_index = WordEmbeddingSimilarityIndex(self.w2v_model)
        similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary)

        similarity = similarity_matrix.inner_product(model_out, reference, normalized=(True, True))

        return similarity


if __name__ == '__main__':
    ts = TitleSimilarity()
    ts.__int__()

    with open('../../data/generated/tom_scott_videos_gpt3_vanilla_v1.csv', 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[1] != '' and row[3] != '':
                print(row[1], 'vs', row[3])

                score = ts.scores_scm(row[1], row[3])

                print()
                print('Score: ', score)
                print()
                print()


