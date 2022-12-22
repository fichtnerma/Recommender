def get_precision(top_n_user_pred, user_threshold=5, user_ratings_count=None):
    recommendation_count = sum((est_r >= user_threshold) for est_r in top_n_user_pred["est_r"])

    true_positive = sum((est_r >= user_threshold and rating >= user_threshold) for rating, est_r in zip(top_n_user_pred["rating"], top_n_user_pred["est_r"]))

    if recommendation_count == 0:
        return 0
    elif user_ratings_count is None or user_ratings_count == 0 or user_ratings_count > recommendation_count:
        return true_positive / recommendation_count
    else:
        return true_positive / user_ratings_count


def get_recall(top_n_user_pred, user_predictions, user_threshold=5, user_ratings_count=None):
    relevant_items_count = sum((rating >= user_threshold) for rating in user_predictions["rating"])

    true_positive = sum((est_r >= user_threshold and rating >= user_threshold) for rating, est_r in zip(top_n_user_pred["rating"], top_n_user_pred["est_r"]))
    if relevant_items_count == 0:
        return 0
    elif user_ratings_count is None or user_ratings_count == 0 or user_ratings_count > relevant_items_count:
        return true_positive / relevant_items_count
    else:
        return true_positive / user_ratings_count


def get_avg_precision(all_ratings, predictions, k=10, use_max_val=False):
    """Get average precision for the provided predictions over all users with ratings

        Args:
                all_ratings (Pandas Dataframe): All available ratings
                predictions (defaultdict): Predictions for each user
                k (int, optional): Amount of recommendations. Defaults to 10.
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Average precision for the provided predictions over all users with ratings
        """

    precision_sum = 0
    for uid, pred_items in predictions.items():
        user_ratings = all_ratings[all_ratings["user_id"] == uid]
        top_k_user_pred = pred_items[:k]
        merged = top_k_user_pred.merge(user_ratings, on="item_id", how="left")

        precision = get_precision(merged, user_ratings["rating"].mean(), user_ratings_count=len(user_ratings) if use_max_val else None)
        precision_sum += precision

    return precision_sum / len(predictions.items())


def get_avg_recall(all_ratings, predictions, k=10, use_max_val=False):
    """Get average recall for the provided predictions over all users with ratings

        Args:
                all_ratings (Pandas Dataframe): All available ratings
                predictions (defaultdict): Predictions for each user
                k (int, optional): Amount of recommendations. Defaults to 10.
                threshold (float, optional): Parameter to define the threshold above which items are considered "good". Defaults to 5.

        Returns:
                float: Average recall for the provided predictions over all users with ratings
        """

    recall_sum = 0
    for idx, (uid, pred_items) in enumerate(predictions.items()):
        user_ratings = all_ratings[all_ratings["user_id"] == uid]
        top_k_user_pred = pred_items[:k]
        merged = top_k_user_pred.merge(user_ratings, on="item_id", how="left")

        recall = get_recall(merged, user_ratings, user_ratings["rating"].mean(), user_ratings_count=len(user_ratings) if use_max_val else None)
        recall_sum += recall

    return recall_sum / len(predictions.items())
