from transformers import pipeline
import csv

classifier = pipeline(
    "text-classification",
    model="Horizon-Labs/multilingual-sentiment-small"
)

reviews = [
    # Positive reviews
    "The product is amazing and works perfectly!",
    "I absolutely love this service. Highly recommended!",
    "Great quality for the price. I am very satisfied.",
    "The experience was excellent from start to finish.",
    "Fast delivery and excellent customer support.",
    "This is one of the best products I have ever purchased.",
    "Everything works as expected. Very happy with my purchase.",
    "The app is easy to use and has a clean interface.",
    "Fantastic experience! I will definitely buy again.",
    "The quality exceeded my expectations. Five stars!",

    # Negative reviews
    "The product broke after just two days of use.",
    "Terrible service. I will never buy from this company again.",
    "The quality is very poor for such a high price.",
    "I am extremely disappointed with this purchase.",
    "The app crashes constantly and is almost unusable.",
    "Customer support was rude and completely unhelpful.",
    "Delivery was late, and the package arrived damaged.",
    "This product does not work as advertised.",
    "A complete waste of money. I regret buying it.",
    "The experience was frustrating from beginning to end.",

    # Neutral reviews
    "The product arrived yesterday and came in a standard box.",
    "I have been using this application for two weeks.",
    "The package contains the product and a user manual.",
    "The service is available from Monday to Friday.",
    "The product has three different operating modes.",
    "I ordered the item online and received it by mail.",
    "The application requires an internet connection.",
    "The device weighs approximately two kilograms.",
    "The website provides information about available products.",
    "I used the service once to complete a transaction."
]

def analyze_review(review):
    result = classifier(review)[0]

    print("\nReview:", review)
    print("Sentiment:", result["label"])
    print(f"Confidence: {result['score']:.2f}")

    return result


def save_results(results):
    with open("results.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow(["comment", "sentiment", "confidence"])

        for review, result in results:
            writer.writerow([
                review,
                result["label"],
                result["score"]
            ])

    print("\nResults saved to results.csv")


def main():
    results = []

    while True:
        print("\n===== REVIEW ANALYZER =====")
        print("1. Analyze all reviews")
        print("2. Choose a review to analyze")
        print("3. Enter a review manually")
        print("4. Show statistics")
        print("5. Save results to CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            for review in reviews:
                result = analyze_review(review)
                results.append((review, result))

            print("\nReviews analyzed:", len(results))
        elif choice == "2":
            print("\n===== REVIEWS =====")

            for i, review in enumerate(reviews, start=1):
                print(f"{i}. {review}")

            try:
                number = int(input("\nEnter review number: "))

                if 1 <= number <= len(reviews):
                    review = reviews[number - 1]
                    result = analyze_review(review)
                    results.append((review, result))
                else:
                    print("Error: invalid review number.")

            except ValueError:
                print("Error: enter a valid number.")

        elif choice == "3":
            review = input("\nEnter your review: ").strip()

            if review:
                result = analyze_review(review)
                results.append((review, result))
            else:
                print("Error: review cannot be empty.")

        elif choice == "4":
            print("\n===== STATISTICS =====")
            print(f"Reviews analyzed: {len(results)}")

            positive_count = sum(
                1 for _, result in results
                if result["label"] == "positive"
            )

            negative_count = sum(
                1 for _, result in results
                if result["label"] == "negative"
            )

            neutral_count = sum(
                1 for _, result in results
                if result["label"] == "neutral"
            )

            print(f"Positive reviews: {positive_count}")
            print(f"Negative reviews: {negative_count}")
            print(f"Neutral reviews: {neutral_count}")

        elif choice == "5":
            if results:
                save_results(results)
            else:
                print("Error: results are empty.")

        elif choice == "0":
            print("Exiting Review Analyzer.")
            break

        else:
            print("Error: invalid menu option.")


if __name__ == "__main__":
    main()


