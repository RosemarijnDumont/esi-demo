
import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Card, CardContent, CardMedia, IconButton, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

// Dummy Food Data
const foodItems = [
  {
    id: 'pizza',
    name: 'Pizza',
    description: 'Delicious pepperoni pizza.',
    price: 15.00,
    image: 'https://via.placeholder.com/150'
  },
  {
    id: 'burger',
    name: 'Burger',
    description: 'Classic beef burger with all the fixings.',
    price: 10.00,
    image: 'https://via.placeholder.com/150'
  },
  {
    id: 'salad',
    name: 'Salad',
    description: 'Fresh garden salad with vinaigrette.',
    price: 8.00,
    image: 'https://via.placeholder.com/150'
  },
];

const officeLocations = [
  { id: 'main_office', name: 'Main Office - Ground Floor' },
  { id: 'annex_building', name: 'Annex Building - 3rd Floor' },
  { id: 'co_working', name: 'Co-working Space - Rooftop' },
];

export const FoodItemCard = ({ item, onQuantityChange }) => {
  const [quantity, setQuantity] = useState(0);

  const handleAdd = () => {
    setQuantity(prev => prev + 1);
    onQuantityChange(item.id, quantity + 1);
  };

  const handleRemove = () => {
    if (quantity > 0) {
      setQuantity(prev => prev - 1);
      onQuantityChange(item.id, quantity - 1);
    }
  };

  return (
    <Card sx={{ display: 'flex', marginBottom: 2 }}>
      <CardMedia
        component="img"
        sx={{ width: 150 }}
        image={item.image}
        alt={item.name}
      />
      <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography gutterBottom variant="h5" component="div">
            {item.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {item.description}
          </Typography>
          <Typography variant="h6" color="text.primary">
            ${item.price.toFixed(2)}
          </Typography>
        </CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', padding: 2 }}>
          <IconButton onClick={handleRemove} color="error" disabled={quantity === 0}>
            <RemoveIcon />
          </IconButton>
          <TextField
            value={quantity}
            inputProps={{ readOnly: true, style: { textAlign: 'center' } }}
            sx={{ width: 50, mx: 1 }}
            size="small"
          />
          <IconButton onClick={handleAdd} color="primary">
            <AddIcon />
          </IconButton>
        </Box>
      </Box>
    </Card>
  );
};

export const LocationSelection = ({ selectedLocation, onLocationChange }) => {
  return (
    <FormControl fullWidth sx={{ marginBottom: 3 }}>
      <InputLabel id="location-select-label">Pickup Location</InputLabel>
      <Select
        labelId="location-select-label"
        id="location-select"
        value={selectedLocation}
        label="Pickup Location"
        onChange={(e) => onLocationChange(e.target.value)}
        required
      >
        {officeLocations.map((location) => (
          <MenuItem key={location.id} value={location.id}>
            {location.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export const OrderSummaryDisplay = ({ orderDetails }) => {
  if (!orderDetails) return null;

  const { items, total, locationName } = orderDetails;

  return (
    <Box sx={{ marginTop: 4, padding: 3, border: '1px solid #ccc', borderRadius: '8px', backgroundColor: '#f9f9f9' }}>
      <Typography variant="h5" gutterBottom>Order Confirmation</Typography>
      <Typography variant="body1">Thank you for your order!</Typography>
      <Typography variant="body1" sx={{ mt: 1 }}>Pickup Location: <strong>{locationName}</strong></Typography>
      <Typography variant="h6" sx={{ mt: 2 }}>Items:</Typography>
      {
        Object.keys(items).length === 0 ? (
          <Typography>No items in your order.</Typography>
        ) : (
          Object.entries(items).map(([itemId, details]) => (
            <Typography key={itemId} variant="body2">
              {details.name} x {details.quantity} - ${details.subtotal.toFixed(2)}
            </Typography>
          ))
        )
      }
      <Typography variant="h6" sx={{ mt: 2 }}>Total: <strong>${total.toFixed(2)}</strong></Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        You will receive a confirmation email shortly.
      </Typography>
    </Box>
  );
};

export const FoodOrderingForm = () => {
  const [quantities, setQuantities] = useState({}); // { itemId: quantity }
  const [selectedLocation, setSelectedLocation] = useState('');
  const [orderSubmitted, setOrderSubmitted] = useState(false);
  const [orderDetails, setOrderDetails] = useState(null);
  const [formErrors, setFormErrors] = useState({ location: false, items: false });

  const handleQuantityChange = (itemId, quantity) => {
    setQuantities(prev => ({
      ...prev,
      [itemId]: quantity,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    let errors = { location: false, items: false };
    let isValid = true;

    if (!selectedLocation) {
      errors.location = true;
      isValid = false;
    }

    const totalItemsOrdered = Object.values(quantities).reduce((acc, qty) => acc + qty, 0);
    if (totalItemsOrdered === 0) {
      errors.items = true;
      isValid = false;
    }

    setFormErrors(errors);

    if (!isValid) {
      return;
    }

    const itemsInOrder = {};
    let totalOrderPrice = 0;

    Object.entries(quantities).forEach(([itemId, quantity]) => {
      if (quantity > 0) {
        const item = foodItems.find(i => i.id === itemId);
        if (item) {
          const subtotal = item.price * quantity;
          itemsInOrder[itemId] = { ...item, quantity, subtotal };
          totalOrderPrice += subtotal;
        }
      }
    });

    const locationName = officeLocations.find(loc => loc.id === selectedLocation)?.name;

    const orderData = {
      items: itemsInOrder,
      total: totalOrderPrice,
      location: selectedLocation,
      locationName: locationName,
      timestamp: new Date().toISOString(),
    };

    // In a real application, you would send orderData to a backend API
    console.log('Order Submitted:', orderData);

    setOrderDetails(orderData);
    setOrderSubmitted(true);
    setQuantities({}); // Clear form after submission
    setSelectedLocation('');
  };

  if (orderSubmitted) {
    return <OrderSummaryDisplay orderDetails={orderDetails} />;
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        maxWidth: 600,
        margin: 'auto',
        padding: 4,
        border: '1px solid #ddd',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
      }}
    >
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Food Order Form - ML6
      </Typography>

      <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
        Select Your Food Items
      </Typography>
      {
        foodItems.map(item => (
          <FoodItemCard
            key={item.id}
            item={item}
            onQuantityChange={handleQuantityChange}
          />
        ))
      }
      {formErrors.items && (
        <Typography color="error" variant="body2" sx={{ mb: 2 }}>
          Please select at least one food item.
        </Typography>
      )}

      <LocationSelection
        selectedLocation={selectedLocation}
        onLocationChange={setSelectedLocation}
      />
      {formErrors.location && (
        <Typography color="error" variant="body2" sx={{ mb: 2 }}>
          Please select a pickup location.
        </Typography>
      )}

      <Button
        type="submit"
        variant="contained"
        size="large"
        sx={{ mt: 3 }}
      >
        Place Order
      </Button>
    </Box>
  );
};
