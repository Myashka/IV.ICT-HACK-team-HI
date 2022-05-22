import emotionRecog_API as emotion
import generationText_API as gen


def predict(text):
    output = emotion.query({'inputs': text})
    emotion_dict = {}

    for i in range(len(output[0])):
        emotion_dict[output[0][i]['label']] = output[0][i]['score']

    sorted_em_dict = {k: v for k, v in sorted(emotion_dict.items(), key=lambda item: item[1], reverse=True)}

    request_text = ""
    keys = list(sorted_em_dict.keys())
    for i in range(8):
        request_text += str(keys[i]) + ", "

    recommendation = gen.query(request_text[:-2])

    return recommendation
