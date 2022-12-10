def get_precision(top_n_user_pred, threshold=5):
    """Calculate Precision for user predictions

        Args:
                top_n_user_pred (Pandas Dataframe, consists of userId, est_r, rating): Top n predictions for a specific user
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Precision for user predictions
        """

    recommendation_count = sum((est_r >= threshold)
                               for est_r in top_n_user_pred["est_r"])

    true_positive = sum((est_r >= threshold and rating >= threshold) for rating,
                        est_r in zip(top_n_user_pred["rating"], top_n_user_pred["est_r"]))

    return true_positive / recommendation_count if recommendation_count != 0 else 0


def get_recall(top_n_user_pred, user_predictions, threshold=5):
    """Calculate Recall for user predictions

        Args:
                top_n_user_pred (Pandas Dataframe, consists of userId, est_r, rating): Top n predictions for a specific user
                user_predictions (Pandas Dataframe): All predictions for a specific user
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Recall for user predictions
        """

    relevant_items_count = sum((est_r >= threshold)
                               for est_r in user_predictions["est_r"])

    true_positive = sum((est_r >= threshold and rating >= threshold) for rating,
                        est_r in zip(top_n_user_pred["rating"], top_n_user_pred["est_r"]))

    return true_positive / relevant_items_count if relevant_items_count != 0 else 0


def get_avg_precision(all_ratings, predictions, k=10, threshold=5):
    """Get average precision for the provided predictions over all users with ratings

        Args:
                all_ratings (Pandas Dataframe): All available ratings
                predictions (defaultdict): Predictions for each user
                k (int, optional): Amount of recommendations. Defaults to 10.
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Average precision for the provided predictions over all users with ratings
        """

    # print(predictions)
    sum = 0
    for uid, pop_items in predictions.items():
        #print("Uid", uid)
        print("Popular items", pop_items)
        user_ratings = all_ratings[all_ratings["userId"] == uid]

        top_k_user_pred = pop_items[:k]

        merged = top_k_user_pred.merge(user_ratings, on="itemId", how="left")

        precision = get_precision(merged, threshold=threshold)
        sum += precision

    return sum / len(predictions.items())


def get_avg_recall(all_ratings, predictions, k=10, threshold=3.5):
    """Get average recall for the provided predictions over all users with ratings

        Args:
                all_ratings (Pandas Dataframe): All available ratings
                predictions (defaultdict): Predictions for each user
                k (int, optional): Amount of recommendations. Defaults to 10.
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Average recall for the provided predictions over all users with ratings
        """

    sum = 0
    for uid, pop_items in predictions.items():
        user_ratings = all_ratings[all_ratings["userId"] == uid]
        top_k_user_pred = pop_items[:k]
        merged = top_k_user_pred.merge(user_ratings, on="itemId", how="left")

        recall = get_recall(merged, pop_items, threshold=threshold)
        sum += recall

    return sum / len(predictions.items())
