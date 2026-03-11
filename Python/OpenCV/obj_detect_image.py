from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

np.set_printoptions(suppress=True)

model = load_model("keras_model.h5", compile=False)

class_names = open("labels.txt", "r").readlines()

image = cv2.imread('controller.jpg')
#image = cv2.imread('card.png')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

image_resize = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
image_input = np.asarray(image_resize, dtype=np.float32).reshape(1, 224, 224, 3)
image_input = (image_input / 127.5) - 1

prediction = model.predict(image_input)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]


text = f"{class_name[2:].strip()} {str(np.round(confidence_score*100))[:-2]} %" 
cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

print("Class:", class_name[2:], end="")
print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

cv2.imshow("Webcam Image", image)
cv2.waitKey(0)

image.release()
cv2.destroyAllWindows()
