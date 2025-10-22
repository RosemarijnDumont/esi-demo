
import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert, ActivityIndicator, StyleSheet } from 'react-native';
import { submitDataForSync } from '../services/dataSyncClient';
import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';

const DataEntryForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!title || !description || !amount) {
      Alert.alert('Validation Error', 'All fields are required.');
      return;
    }

    setLoading(true);
    try {
      const entryData = {
        id: uuidv4(), // Generate a unique ID for the entry
        title,
        description,
        amount: parseFloat(amount),
        timestamp: new Date().toISOString(),
        userId: 'someUserId', // Replace with actual user ID from authentication context
      };

      const result = await submitDataForSync(entryData, 'entry');

      if (result.status === 'synced') {
        Alert.alert('Success', 'Entry added and synced successfully!');
        setTitle('');
        setDescription('');
        setAmount('');
      } else if (result.status === 'queued_for_retry') {
        Alert.alert('Warning', 'Entry added, but failed to sync immediately. It will be retried.');
        setTitle('');
        setDescription('');
        setAmount('');
      } else if (result.status === 'saved_locally_offline') {
        Alert.alert('Offline', 'Entry saved locally. It will sync once you are online.');
        setTitle('');
        setDescription('');
        setAmount('');
      }
    } catch (error) {
      console.error('Submission error:', error);
      Alert.alert('Error', 'Failed to submit entry. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Add New Entry</Text>
      <TextInput
        style={styles.input}
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
      />
      <TextInput
        style={styles.input}
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
        multiline
      />
      <TextInput
        style={styles.input}
        placeholder="Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
      />
      <Button
        title={loading ? "Submitting..." : "Submit Entry"}
        onPress={handleSubmit}
        disabled={loading}
      />
      {loading && <ActivityIndicator size="small" color="#0000ff" style={styles.loadingIndicator} />}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
    borderRadius: 8,
    margin: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 5,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    marginBottom: 15,
    borderRadius: 5,
    fontSize: 16,
  },
  loadingIndicator: {
    marginTop: 10,
  },
});

export default DataEntryForm;
