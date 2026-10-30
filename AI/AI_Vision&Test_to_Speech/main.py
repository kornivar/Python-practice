from transformers import BlipProcessor, BlipForConditionalGeneration, pipeline
from PIL import Image
import torch
import scipy.io.wavfile
import os



processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)



def describe_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")

        inputs = processor(image, return_tensors="pt")

        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=100)

        description = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        print("\n===== IMAGE DESCRIPTION =====")
        print(description)

        return description

    except FileNotFoundError:
        print("Error: image file not found.")

    except Exception as e:
        print(f"Error: {e}")


def save_description(text):
    with open("descriptions.txt", "a", encoding="utf-8") as file:
        file.write(text + "\n")

    print("Description saved to descriptions.txt")



synthesizer = pipeline(
    "text-to-speech",
    model="facebook/mms-tts-eng"
)


def generate_speech(text):
    try:
        file_name = input("\nEnter audio file name: ").strip()

        if not file_name:
            print("Error: file name cannot be empty.")
            return

        if not file_name.lower().endswith(".wav"):
            file_name += ".wav"

        os.makedirs("output", exist_ok=True)

        file_path = os.path.join("output", file_name)

        result = synthesizer(text)

        scipy.io.wavfile.write(
            file_path,
            rate=result["sampling_rate"],
            data=result["audio"].squeeze()
        )

        print(f"Audio saved to: {os.path.abspath(file_path)}")

    except Exception as e:
        print(f"Error generating speech: {e}")




def main():
    while True:
        print("\n===== IMAGE DESCRIBER =====")
        print("1. Describe an image")
        print("0. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            image_path = input("\nEnter image path: ").strip().strip('"')

            if os.path.isfile(image_path):
                text = describe_image(image_path)

                if text:
                    save_description(text)

                    print("\nGenerating speech...")
                    generate_speech(text)
                else:
                    print("Error: could not generate description.")

            else:
                print("Error: invalid image path.")

        elif choice == "0":
            print("Exiting Image Describer.")
            break

        else:
            print("Error: invalid menu option.")


if __name__ == "__main__":
    main()

