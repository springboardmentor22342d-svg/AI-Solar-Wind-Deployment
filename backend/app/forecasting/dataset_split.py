from sklearn.model_selection import train_test_split


def split_dataset(
    X,
    y,
    train_size=0.70,
    validation_size=0.15,
    test_size=0.15,
    random_state=42,
):
    """
    Split dataset into training, validation, and testing sets.

    Returns:
        X_train, X_val, X_test,
        y_train, y_val, y_test
    """

    if abs(train_size + validation_size + test_size - 1.0) > 1e-6:
        raise ValueError("Split ratios must sum to 1.")

    # First split: Train vs Temp
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=(validation_size + test_size),
        random_state=random_state,
        shuffle=True,
    )

    # Second split: Validation vs Test
    val_ratio = validation_size / (validation_size + test_size)

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        train_size=val_ratio,
        random_state=random_state,
        shuffle=True,
    )

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    )