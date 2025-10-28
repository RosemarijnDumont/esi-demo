
import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Heading,
  VStack,
  Alert,
  AlertIcon,
  CloseButton,
  Spinner,
  Text,
  Link,
} from '@chakra-ui/react';
import axios from 'axios'; // For API calls

const SSOConfiguration = () => {
  const [metadataXml, setMetadataXml] = useState('');
  const [attributeMapping, setAttributeMapping] = useState('');
  const [ssoEnabled, setSsoEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  // In a real application, you'd fetch this from environment variables or a config file
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api'; 

  useEffect(() => {
    fetchSsoConfiguration();
  }, []);

  const fetchSsoConfiguration = async () => {
    setLoading(true);
    setErrorMessage('');
    setSuccessMessage('');
    try {
      const response = await axios.get(`${API_BASE_URL}/trial-sso/config`);
      const config = response.data;
      setMetadataXml(config.metadataXml || '');
      setAttributeMapping(config.attributeMapping || '');
      setSsoEnabled(config.ssoEnabled || false);
    } catch (error) {
      console.error('Error fetching SSO configuration:', error);
      setErrorMessage('Failed to fetch SSO configuration. Please try again.');
    }
    setLoading(false);
  };

  const handleSave = async () => {
    setLoading(true);
    setErrorMessage('');
    setSuccessMessage('');

    // Client-side validation
    if (!metadataXml.trim()) {
      setErrorMessage('IdP Metadata XML cannot be empty.');
      setLoading(false);
      return;
    }

    try {
      const payload = {
        metadataXml: metadataXml.trim(),
        attributeMapping: attributeMapping.trim(),
        ssoEnabled: ssoEnabled,
      };
      await axios.post(`${API_BASE_URL}/trial-sso/config`, payload);
      setSuccessMessage('SSO configuration saved successfully!');
    } catch (error) {
      console.error('Error saving SSO configuration:', error);
      setErrorMessage(
        error.response?.data?.message ||
          'Failed to save SSO configuration. Please check your inputs.'
      );
    }
    setLoading(false);
  };

  const handleEnableDisableSso = async () => {
    setLoading(true);
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const newSsoEnabledState = !ssoEnabled;
      await axios.patch(`${API_BASE_URL}/trial-sso/toggle`, {
        ssoEnabled: newSsoEnabledState,
      });
      setSsoEnabled(newSsoEnabledState);
      setSuccessMessage(
        `SSO ${newSsoEnabledState ? 'enabled' : 'disabled'} successfully!`
      );
    } catch (error) {
      console.error('Error toggling SSO:', error);
      setErrorMessage(
        error.response?.data?.message ||
          `Failed to ${ssoEnabled ? 'disable' : 'enable'} SSO. Please try again.`
      );
    }
    setLoading(false);
  };

  return (
    <Box p={8} maxWidth="800px" mx="auto">
      <Heading as="h2" size="xl" mb={6}>
        Trial SSO Configuration
      </Heading>

      {loading && (
        <Alert status="info" mb={4}>
          <AlertIcon />
          <Spinner size="sm" mr={2} /> Loading configuration...
        </Alert>
      )}

      {successMessage && (
        <Alert status="success" mb={4}>
          <AlertIcon />
          {successMessage}
          <CloseButton
            position="absolute"
            right="8px"
            top="8px"
            onClick={() => setSuccessMessage('')}
          />
        </Alert>
      )}

      {errorMessage && (
        <Alert status="error" mb={4}>
          <AlertIcon />
          {errorMessage}
          <CloseButton
            position="absolute"
            right="8px"
            top="8px"
            onClick={() => setErrorMessage('')}
          />
        </Alert>
      )}

      <VStack spacing={6} align="stretch">
        <Text fontSize="md">
          Configure Single Sign-On (SSO) for your trial account. Upload your
          Identity Provider (IdP) metadata XML to enable SAML-based
          authentication.
        </Text>
        <Text fontSize="md">
          For detailed instructions, please refer to our{' '}
          <Link color="teal.500" href="/docs/sso-trial" isExternal>
            SSO for Trial Accounts Documentation
          </Link>
          .
        </Text>

        <FormControl id="metadataXml" isRequired>
          <FormLabel>IdP Metadata XML</FormLabel>
          <Textarea
            value={metadataXml}
            onChange={(e) => setMetadataXml(e.target.value)}
            placeholder="Paste your Identity Provider (IdP) Metadata XML here"
            rows={10}
            fontFamily="monospace"
            borderColor="gray.300"
            _hover={{ borderColor: 'gray.400' }}
            _focus={{ borderColor: 'blue.500', boxShadow: 'outline' }}
          />
          <Text fontSize="sm" mt={2} color="gray.600">
            Your IdP Metadata XML contains the necessary information for our
            service provider to communicate with your identity provider.
          </Text>
        </FormControl>

        <FormControl id="attributeMapping">
          <FormLabel>Attribute Mappings (Optional)</FormLabel>
          <Input
            value={attributeMapping}
            onChange={(e) => setAttributeMapping(e.target.value)}
            placeholder="e.g., email=mail, firstName=givenName"
          />
          <Text fontSize="sm" mt={2} color="gray.600">
            Define how attributes from your IdP map to user attributes in our
            system (e.g., `ourAttributeName=IdPAttributeName`). Consult
            documentation for supported attributes.
          </Text>
        </FormControl>

        <Button
          colorScheme="blue"
          onClick={handleSave}
          isLoading={loading}
          loadingText="Saving..."
          alignSelf="flex-start"
        >
          Save Configuration
        </Button>

        <Box borderTop="1px" borderColor="gray.200" pt={6} mt={6}>
          <Heading as="h3" size="lg" mb={4}>
            SSO Status
          </Heading>
          <Text mb={4}>
            Current SSO Status: {' '}
            <Text as="span" fontWeight="bold" color={ssoEnabled ? 'green.500' : 'red.500'}>
              {ssoEnabled ? 'Enabled' : 'Disabled'}
            </Text>
          </Text>
          <Button
            colorScheme={ssoEnabled ? 'red' : 'green'}
            onClick={handleEnableDisableSso}
            isLoading={loading}
            loadingText={ssoEnabled ? 'Disabling...' : 'Enabling...'}
          >
            {ssoEnabled ? 'Disable SSO' : 'Enable SSO'}
          </Button>
          <Text fontSize="sm" mt={2} color="gray.600">
            Toggling this will immediately enable or disable SSO for your trial account.
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default SSOConfiguration;

