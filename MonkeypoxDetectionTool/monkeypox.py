import numpy as np

model = load_model('/Users/rhesaurus/Documents/Python ML/Covid-19 Detection using CNN/model.hdf5/')

class run_model():
    def __init__(self)-> None:
        pass

    def model_predict(self, img_path):
        img = image.load_img(str(img_path), target_size = (224,224))

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis = 0)
        img_data = preprocess_input(x)

        classes = model.predict(img_data)

        classwise_result = vgg_model.predict(x)
        result = classwise_result[0][3]


        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)


        if int(result) == 1:
            return "Person is affected by Monkeypox with an accuracy of ", result, "%")
        else:
            return "Person is not affected by Monkeypox"
