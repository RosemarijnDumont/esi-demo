
import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import SSOConfiguration from './components/SSOConfiguration';

function App() {
  return (
    <ChakraProvider>
      <SSOConfiguration />
    </ChakraProvider>
  );
}

export default App;
