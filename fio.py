from PIL import Image
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
traits = ['ValueExtraversion', 'ValueAgreeableness', 'ValueConscientiousness', 'ValueNeurotisicm', 'ValueOpenness']



def load_and_preprocess_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((128, 128))
    return np.array(image) / 255.0


def create_image_to_label_mapping(df_labels, dataset_folder_path):
    # Create a dictionary to map video prefixes to their corresponding rows in the DataFrame
    video_prefix_to_label = {}
    for _, row in df_labels.iterrows():
        video_name_prefix = row['VideoName'].split('.')[0]
        video_prefix_to_label[video_name_prefix] = row.drop('VideoName').to_dict()

    # Now map the images to labels using the optimized dictionary
    image_to_label_mapping_optimized = {}
    selfie_folders = ['portrait-personality-1', 'portrait-personality-2', 'portrait-personality-3']

    for folder in selfie_folders:
        folder_path = Path(dataset_folder_path) / folder
        for image_path in folder_path.iterdir():
            # Extract the video name prefix from the image file name
            video_name_prefix = image_path.name.split('.')[0]
            if video_name_prefix in video_prefix_to_label:
                image_to_label_mapping_optimized[str(image_path)] = video_prefix_to_label[video_name_prefix]
                
    return image_to_label_mapping_optimized


def create_model(traits):
    image_input = Input(shape=(128, 128, 3), name='ImageInput')
    x = Conv2D(32, (3, 3), activation='relu')(image_input)
    x = MaxPooling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = MaxPooling2D((2, 2))(x)
    x = Flatten()(x)

    output_layers = []
    for trait in traits:
        trait_output = Dense(1, activation='linear', name=f"{trait}Output")(x)
        output_layers.append(trait_output)

    model = Model(inputs=image_input, outputs=output_layers)
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    return model


if __name__ == "__main__":

    df_labels = pd.read_csv("C:\\Users\\admin\\Desktop\\fio\\personality-master\\dataset\\bigfive_labels.csv")
    dataset_folder_path = "C:\\Users\\admin\\Desktop\\fio\\personality-master\\dataset"
    image_to_label_mapping = create_image_to_label_mapping(df_labels, dataset_folder_path)

    image_paths = list(image_to_label_mapping.keys())
    labels = [image_to_label_mapping[path] for path in image_paths]
    images = [load_and_preprocess_image(path) for path in image_paths]
    
    print(f"Number of images: {len(images)}")
    print(f"Number of labels: {len(labels)}")

    X_train, X_temp, y_train, y_temp = train_test_split(images, labels, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    y_train_df = pd.DataFrame(y_train)
    y_val_df = pd.DataFrame(y_val)

    model = create_model(traits)
    model.summary()
    print("Sample y_train item:", y_train[0])

    train_data = {f"{trait}Output": y_train_df[trait].values for trait in traits}
    val_data = {f"{trait}Output": y_val_df[trait].values for trait in traits}

    model.fit(
        np.array(X_train),
        train_data,
        validation_data=(np.array(X_val), val_data),
        epochs=10
    )

    model.save("C:\\Users\\admin\\Desktop\\fio\\tmp")
