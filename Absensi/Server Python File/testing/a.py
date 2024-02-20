from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import tensorflow as tf

# Memuat model GPT-2 dan tokenizer
model_gpt2 = TFGPT2LMHeadModel.from_pretrained('gpt2')
tokenizer_gpt2 = GPT2Tokenizer.from_pretrained('gpt2')

# Inisialisasi konteks percakapan
konteks = ""

while True:
    # Menerima input dari pengguna
    pertanyaan_user = input("Tanyakan sesuatu (atau ketik 'selesai' untuk mengakhiri): ")

    if pertanyaan_user.lower() == 'selesai':
        break

    # Menyiapkan input dengan menyertakan konteks percakapan sebelumnya
    input_text = f"{konteks} Pertanyaan: {pertanyaan_user}\nJawaban:"

    # Tokenisasi input
    input_ids = tokenizer_gpt2.encode(input_text, return_tensors='tf')

    # Membuat attention mask
    attention_mask = tf.ones_like(input_ids)

    # Membuat prediksi dengan mengatasi peringatan `do_sample`
    output = model_gpt2.generate(
        input_ids, 
        max_length=80, 
        num_return_sequences=1, 
        do_sample=True, 
        temperature=0.8, 
        attention_mask=attention_mask
    )

    # Mendekode output menjadi teks
    jawaban_gpt2 = tokenizer_gpt2.decode(output[0], skip_special_tokens=True)

    # Menyimpan konteks percakapan untuk penggunaan berikutnya
    konteks += f"Pertanyaan: {pertanyaan_user}\nJawaban: {jawaban_gpt2}\n"

    # Menampilkan jawaban dari GPT-2
    print(f"Jawaban dari GPT-2: {jawaban_gpt2}")
