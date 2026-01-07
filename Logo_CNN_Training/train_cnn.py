import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# CHANGE THIS to your real dataset path
dataset_path = r"C:\Users\sohs2\OneDrive\Desktop\Logo_CNN_Training\dataset"

IMG_SIZE = 128
BATCH_SIZE = 32

# --------- LOAD DATA ----------
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation",
    shuffle=False
)

print("Class labels:", train_data.class_indices)

# --------- CNN MODEL ----------
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    train_data,
    epochs=12,
    validation_data=val_data
)

# --------- SAVE MODEL ----------
model.save("logo_counterfeit_cnn.h5")
print("✅ Model saved as logo_counterfeit_cnn.h5")

# --------- ACCURACY GRAPH ----------
plt.figure()
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("Accuracy Graph")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.grid()
plt.savefig("accuracy_graph.png", dpi=300)
plt.close()

# --------- LOSS GRAPH ----------
plt.figure()
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("Loss Graph")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.grid()
plt.savefig("loss_graph.png", dpi=300)
plt.close()

print("✅ Accuracy and Loss graphs saved")

# --------- CONFUSION MATRIX ----------
val_data.reset()
y_true = []
y_pred = []

for i in range(len(val_data)):
    x, y = val_data[i]
    preds = model.predict(x)
    y_true.extend(y)
    y_pred.extend((preds > 0.5).astype(int).reshape(-1))

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=list(train_data.class_indices.keys()))
disp.plot()
plt.savefig("confusion_matrix.png", dpi=300)
plt.close()

print("✅ Confusion matrix saved")
