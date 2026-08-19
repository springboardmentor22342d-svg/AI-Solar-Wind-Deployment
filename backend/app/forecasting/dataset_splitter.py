from sklearn.model_selection import train_test_split


class DatasetSplitter:

    def split(self, X, y):

        # Step 1: Train (70%) and Temp (30%)
        X_train, X_temp, y_train, y_temp = train_test_split(
            X,
            y,
            test_size=0.30,
            random_state=42
        )

        # Step 2: Validation (15%) and Test (15%)
        X_validation, X_test, y_validation, y_test = train_test_split(
            X_temp,
            y_temp,
            test_size=0.50,
            random_state=42
        )

        return {
            "X_train": X_train,
            "X_validation": X_validation,
            "X_test": X_test,
            "y_train": y_train,
            "y_validation": y_validation,
            "y_test": y_test
        }