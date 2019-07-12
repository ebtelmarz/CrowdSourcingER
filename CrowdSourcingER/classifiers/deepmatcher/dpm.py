import deepmatcher as dm
import py_entitymatching as em
import os
import config

def dm_train(df):

    split_path = config.PATHS["deepmatcher_training_folder"]

    # Split labeled data into train, valid, and test csv files to disk, with the split ratio of 3:1:1.
    dm.data.split(df, split_path, 'train.csv', 'valid.csv', 'test.csv',\
                  [3, 1, 1])

    train, validation, test = dm.data.process(
        path=split_path,
        cache='train_cache.pth',
        train='train.csv',
        validation='valid.csv',
        test='test.csv',
        left_prefix = 'ltable',
        right_prefix = 'rtable',
        label_attr='label',
        id_attr = '_id',
        ignore_columns=('ltable_id', 'rtable_id'))

    #Create a hybrid model.
    model = dm.MatchingModel(attr_summarizer='hybrid')

    # Train the hybrid model with 10 training epochs, batch size of 16, positive-to-negative
    # ratio to be 3. We save the best model (with the
    # highest F1 score on the validation set) to 'hybrid_model.pth'.
    model.run_train(
        train,
        validation,
        epochs=3,
        batch_size=16,
        best_save_path=config.PATHS['deepmatcher_model'],
        pos_neg_ratio=10)


    # Evaluate the accuracy on the test data.
    print (model.run_eval(test))
    return model

def dm_prediction(model):

    #model = dm.MatchingModel(attr_summarizer='hybrid')
    #model.load_state(os.path.join(".","classifiers","training_files","hybrid_model.pth"))

    # Load the candidate set. Note that the trained model is an input parameter as we need to trained
    # model for candidate set preprocessing.
    candidate = dm.data.process_unlabeled(
        path=config.PATHS["deepmatcher_unlabeled"],
        trained_model=model,
        ignore_columns=('ltable_id', 'rtable_id'))
    # Predict the pairs in the candidate set and return a dataframe containing the pair id with
    # the score of being a match.
    return model.run_prediction(candidate, output_attributes=list(candidate.get_raw_table().columns))
