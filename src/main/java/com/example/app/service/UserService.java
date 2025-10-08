package com.example.app.service;

import com.example.app.model.User;
import com.example.app.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Cacheable(value = "users", key = "#id")
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    @CacheEvict(value = "users", allEntries = true)
    @Transactional
    public User saveUser(User user) {
        return userRepository.save(user);
    }

    // Optimized method for dashboard, leveraging the cached repository query
    public List<User> getActiveUsersForDashboard() {
        return userRepository.findActiveUsersForDashboard();
    }

    // Example of a cached method using query parameters
    public List<User> getUsersByStatus(String status) {
        return userRepository.findByStatus(status);
    }
}
