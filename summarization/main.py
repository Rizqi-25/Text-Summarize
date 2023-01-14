from flask import Flask, render_template, request
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import operator
import string


class summarize:

    def get_summary(self, input, max_sentences):
        sentences_original = sent_tokenize(input)

        # Hapus semua tab spacing, dan baris baru
        if (max_sentences > len(sentences_original)):
            print(
                "Error, jumlah kalimat yang diminta melebihi jumlah kalimat yang dimasukkan")

        # menghapus white space di depan dan di belakang kalimat
        s = input.strip('\t\n')

        # Hapus tanda baca, tab, baris baru, dan lowercase semua kata, lalu melakukan word tokenize
        words = word_tokenize(s.lower())

        sentence = sent_tokenize(s.lower())

        stop_words = set(stopwords.words("english"))  # membuat stopwords
        punc = set(string.punctuation)

        # Remove all stop words and punctuation from word list.
        filtered_words = []
        for w in words:
            if w not in stop_words and w not in punc:
                filtered_words.append(w)
        total_words = len(filtered_words)

        # Menentukan frekuensi setiap kata yang disaring dan
        # menambahkan kata dan frekuensinya ke dictionary
        word_frequency = {}
        output_sentence = []

        for w in filtered_words:
            if w in word_frequency.keys():
                word_frequency[w] += 1.0  # increment the value: frequency
            else:
                word_frequency[w] = 1.0  # add the word to dictionary

        # Pembobotan kata
        for word in word_frequency:
            word_frequency[word] = (word_frequency[word]/total_words)

        # menyimpan kata-kata yang paling sering muncul di setiap kalimat dan tambahkan jumlah nilai frekuensi setelah dilakukan pembobotan.
        # indexing sentences
        tracker = [0.0] * len(sentences_original)
        for i in range(0, len(sentences_original)):
            for j in word_frequency:
                if j in sentences_original[i]:
                    tracker[i] += word_frequency[j]

        # Ambil kalimat yang memiliki pembobotan paling besar dan hasil indexingnya, lalu tambahkan kalimat tersebut ke output kalimat.
        for i in range(0, len(tracker)):

            # Extract index dengan nilai pembobotan freq tertinggi dari tracker
            index, value = max(enumerate(tracker), key=operator.itemgetter(1))
            if (len(output_sentence)+1 <= max_sentences) and (sentences_original[index] not in output_sentence):
                output_sentence.append(sentences_original[index])
            if len(output_sentence) > max_sentences:
                break

            # Hapus kalimat yang sudah diambil sebelumnya dari tracker, agar kalimat yang diambil selanjutnya memiliki pembobotan freq tertinggi
            tracker.remove(tracker[index])

        sorted_output_sent = self.sort_sentences(
            sentences_original, output_sentence)
        return (sorted_output_sent)

    # @def sort_senteces:
    # Dari output kalimat, urutkan kalimat-kalimat tersebut sehingga mereka muncul dalam urutan teks masukan yang diberikan.

    def sort_sentences(self, original, output):
        sorted_sent_arr = []
        sorted_output = []
        for i in range(0, len(output)):
            if(output[i] in original):
                sorted_sent_arr.append(original.index(output[i]))
        sorted_sent_arr = sorted(sorted_sent_arr)

        for i in range(0, len(sorted_sent_arr)):
            sorted_output.append(original[sorted_sent_arr[i]])
        print(sorted_sent_arr)
        return sorted_output


app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/templates', methods=['POST'])
def original_text_form():
    title = "Summarizer"
    text = request.form['input_text']  # Text dari form input html
    max_value = sent_tokenize(text)
    # Jumlah kalimat yang diminta untuk dibuatkan rangkuman
    num_sent = int(request.form['num_sentences'])
    sum1 = summarize()
    summary = sum1.get_summary(text, num_sent)
    print(summary)
    return render_template("index.html", title=title, original_text=text, output_summary=summary, num_sentences=max_value)


@app.route('/')
def homepage():
    title = "Text Summarizer"
    return render_template("index.html", title=title)

# @app.route('/templates', methods=['POST'])
# def get_started():
#     title = "Get Started"
#     return render_template("get_started.html", title=title)

@app.route('/templates')
def about():
    title = "About"
    return render_template("about_us.html", title=title)


if __name__ == "__main__":
    app.debug = True
    app.run()
