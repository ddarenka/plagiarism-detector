from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Lambda
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import Adam

def create_siamese_network(vocab_size, max_length, embedding_dim, lstm_units):
    # Shared embedding layer
    embedding_layer = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length)
    
    # Shared LSTM layer
    lstm_layer = LSTM(lstm_units)

    # Define two input layers
    input_a = Input(shape=(max_length,))
    input_b = Input(shape=(max_length,))
    
    # Reuse the LSTM layer for both inputs
    processed_a = lstm_layer(embedding_layer(input_a))
    processed_b = lstm_layer(embedding_layer(input_b))
    
    # Calculate the absolute difference between the processed inputs
    distance = Lambda(lambda tensors: K.abs(tensors[0] - tensors[1]))([processed_a, processed_b])
    
    # Dense layer to output similarity score
    outputs = Dense(1, activation='sigmoid')(distance)
    
    # Construct the model
    model = Model(inputs=[input_a, input_b], outputs=outputs)
    
    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    
    return model

