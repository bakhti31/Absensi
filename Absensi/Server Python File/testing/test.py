import openai

# Ganti OPENAI_API_KEY dengan kunci API OpenAI Anda
openai.api_key = 'OPENAI_API_KEY'

def tanya_jawab_gpt3(pertanyaan, konteks_sebelumnya=""):
    prompt = f"{konteks_sebelumnya}Pertanyaan: {pertanyaan}\nJawaban:"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        n=1,
        stop=None
    )

    jawaban = response['choices'][0]['text']
    return jawaban, f"{konteks_sebelumnya}Pertanyaan: {pertanyaan}\nJawaban: {jawaban}\n"

# Inisialisasi konteks percakapan
konteks = ""

while True:
    pertanyaan_user = input("Tanyakan sesuatu (atau ketik 'selesai' untuk mengakhiri): ")

    if pertanyaan_user.lower() == 'selesai':
        break

    jawaban_gpt3, konteks = tanya_jawab_gpt3(pertanyaan_user, konteks)

    print(f"Jawaban dari GPT-3: {jawaban_gpt3}")
