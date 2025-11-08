import React, { useState, useRef } from 'react';
import { View, StyleSheet, Alert, TouchableOpacity, Text } from 'react-native';
import { Camera, CameraType } from 'expo-camera';
import { Button, ActivityIndicator, Menu, TextInput } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';
import { useAnalyzeImageMutation } from '../services/api';
import { Ionicons } from '@expo/vector-icons';

type CameraScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Camera'>;

export default function CameraScreen() {
  const [type, setType] = useState(CameraType.back);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const [isProcessing, setIsProcessing] = useState(false);
  const [cropType, setCropType] = useState('lettuce');
  const [detectionPrompt, setDetectionPrompt] = useState('');
  const [menuVisible, setMenuVisible] = useState(false);
  const cameraRef = useRef<Camera>(null);
  const navigation = useNavigation<CameraScreenNavigationProp>();
  const [analyzeImage] = useAnalyzeImageMutation();

  const cropTypes = ['lettuce', 'basil', 'tomato', 'pepper', 'microgreens'];

  if (!permission) {
    return <View style={styles.container}><ActivityIndicator /></View>;
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button mode="contained" onPress={requestPermission}>
          Grant Permission
        </Button>
      </View>
    );
  }

  const toggleCameraType = () => {
    setType(current =>
      current === CameraType.back ? CameraType.front : CameraType.back
    );
  };

  const takePicture = async () => {
    if (!cameraRef.current || isProcessing) return;

    if (!detectionPrompt.trim()) {
      Alert.alert('Missing Information', 'Please enter what you want to detect (e.g., "nitrogen stress", "disease")');
      return;
    }

    try {
      setIsProcessing(true);
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.8,
        base64: true,
      });

      if (!photo.uri) {
        Alert.alert('Error', 'Failed to capture image');
        setIsProcessing(false);
        return;
      }

      // Send image to backend for analysis
      try {
        const result = await analyzeImage({
          image: photo.base64 || '',
          uri: photo.uri,
          cropType,
          prompt: detectionPrompt,
        }).unwrap();

        // Navigate to results screen
        navigation.replace('Result', {
          testId: result.id,
          imageUri: photo.uri,
        });
      } catch (error: any) {
        Alert.alert(
          'Analysis Failed',
          error.data?.message || 'Failed to analyze crop image. Please try again.',
          [{ text: 'OK' }]
        );
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to take picture');
      console.error('Camera error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        <Menu
          visible={menuVisible}
          onDismiss={() => setMenuVisible(false)}
          anchor={
            <Button
              mode="outlined"
              onPress={() => setMenuVisible(true)}
              style={styles.cropSelector}
            >
              Crop: {cropType.charAt(0).toUpperCase() + cropType.slice(1)}
            </Button>
          }
        >
          {cropTypes.map((type) => (
            <Menu.Item
              key={type}
              onPress={() => {
                setCropType(type);
                setMenuVisible(false);
              }}
              title={type.charAt(0).toUpperCase() + type.slice(1)}
            />
          ))}
        </Menu>

        <TextInput
          mode="outlined"
          label="What to detect (e.g., nitrogen stress)"
          value={detectionPrompt}
          onChangeText={setDetectionPrompt}
          style={styles.promptInput}
          placeholder="e.g., nitrogen-stressed leaves, disease"
        />
      </View>

      <Camera style={styles.camera} type={type} ref={cameraRef}>
        <View style={styles.overlay}>
          <View style={styles.frame} />
          <Text style={styles.guideText}>
            Position crop leaves in frame
          </Text>
          <Text style={styles.guideSubtext}>
            Ensure good lighting for best results
          </Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.flipButton}
            onPress={toggleCameraType}
            disabled={isProcessing}
          >
            <Ionicons name="camera-reverse" size={32} color="white" />
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.captureButton, isProcessing && styles.captureButtonDisabled]}
            onPress={takePicture}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <ActivityIndicator color="white" />
            ) : (
              <View style={styles.captureButtonInner} />
            )}
          </TouchableOpacity>

          <View style={styles.flipButton} />
        </View>
      </Camera>
    </View>
  );
}

const styles = StyleSheet.Create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  inputContainer: {
    backgroundColor: '#fff',
    padding: 12,
    zIndex: 1000,
  },
  cropSelector: {
    marginBottom: 8,
  },
  promptInput: {
    backgroundColor: '#fff',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
    color: '#fff',
  },
  camera: {
    flex: 1,
    width: '100%',
  },
  overlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  frame: {
    width: 300,
    height: 200,
    borderWidth: 3,
    borderColor: '#4CAF50',
    borderRadius: 8,
    backgroundColor: 'transparent',
  },
  guideText: {
    color: '#fff',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 10,
    borderRadius: 5,
  },
  guideSubtext: {
    color: '#fff',
    fontSize: 12,
    marginTop: 8,
    textAlign: 'center',
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 6,
    borderRadius: 5,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 30,
    paddingBottom: 40,
    backgroundColor: 'transparent',
  },
  flipButton: {
    width: 50,
    height: 50,
    justifyContent: 'center',
    alignItems: 'center',
  },
  captureButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'rgba(76,175,80,0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 5,
    borderColor: '#4CAF50',
  },
  captureButtonDisabled: {
    opacity: 0.5,
  },
  captureButtonInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#4CAF50',
  },
});
