import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Text, TextInput } from 'react-native-paper';
import { Camera, CameraType } from 'expo-camera';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { RootStackParamList } from '../navigation/AppNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'Camera'>;

const CameraScreen = ({ navigation }: Props) => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [prompt, setPrompt] = useState('nitrogen stress');
  const cameraRef = useRef<Camera>(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleCapture = async () => {
    if (cameraRef.current) {
      // const photo = await cameraRef.current.takePictureAsync();
      console.log('Photo captured, prompt:', prompt);
      // TODO: Send photo and prompt to backend API
      // On success, navigate to results:
      // navigation.navigate('Result', { analysisId: 'some-id-from-api' });
    }
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <Camera style={styles.camera} type={CameraType.back} ref={cameraRef} />
      <View style={styles.controls}>
        <TextInput label="Detection Prompt" value={prompt} onChangeText={setPrompt} />
        <Button icon="camera" mode="contained" onPress={handleCapture}>Capture and Analyze</Button>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  controls: { padding: 16, gap: 10 },
});

export default CameraScreen;