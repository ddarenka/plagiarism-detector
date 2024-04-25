
from data_preprocesiing import siamese_preprocessing
from models.siamese import create_siamese_network


dataset_path = 'path.json'

#DataPreprocessing 
X1_train, X1_test, X2_train, X2_test, y_train, y_test = siamese_preprocessing.preprocess_data(dataset_path)

# Model parameters
vocab_size = 10000  # Adjust based on your tokenizer
max_length = 200  # Same as in the preprocessing step
embedding_dim = 50  # Can be adjusted
lstm_units = 64  # Can be adjusted

# Create the Siamese Network model
model = create_siamese_network(vocab_size, max_length, embedding_dim, lstm_units)

history = model.fit(
    [X1_train, X2_train], y_train,
    validation_data=([X1_test, X2_test], y_test),
    batch_size=32,
    epochs=10
)
# Evaluate the model on the test set
test_loss, test_acc = model.evaluate([X1_test, X2_test], y_test)
print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")