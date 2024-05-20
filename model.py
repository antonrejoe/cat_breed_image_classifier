import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

# Load the processor and model
processor = AutoImageProcessor.from_pretrained("dima806/cat_breed_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/cat_breed_image_detection")

def predict_class(image_path):
    '''
    Predict and render the class of a given image 
    '''
    # Open and process the image
    image = Image.open(image_path).convert('RGB')
    inputs = processor(images=image, return_tensors="pt")

    # Predict the probability across all output classes
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the logits (predictions)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

    # Get the labels
    labels = model.config.id2label
    predicted_label = labels[predicted_class_idx]

    # Get the probability
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_probability = probabilities[0, predicted_class_idx].item()

    # Print results
    print(f"Logits: {logits}")
    print(f"Predicted class index: {predicted_class_idx}")
    print(f"Predicted class label: {predicted_label}")
    print(f"Predicted class probability: {predicted_probability:.4f}")

    return predicted_label, predicted_probability

if __name__ == '__main__':
    ''' For test '''
    # Load an image from file
    image_path = "static/img/image.jpg"
    prediction, percentage = predict_class(image_path)
    print(f"Prediction: {prediction}, Probability: {percentage:.4f}")
