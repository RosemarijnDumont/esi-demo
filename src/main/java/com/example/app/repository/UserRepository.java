package com.example.app.repository;

import com.example.app.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.cache.annotation.Cacheable;

import java.util.List;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @Cacheable(value = "users", key = "#status")
    List<User> findByStatus(String status);

    @Cacheable(value = "users", key = "'activeUsersDashboard'")
    @Query("SELECT u FROM User u WHERE u.status = 'active' ORDER BY u.createdAt DESC")
    List<User> findActiveUsersForDashboard();

    @Query(value = """
        SELECT u.*, up.product_id
        FROM users u
        JOIN user_products up ON u.id = up.user_id
        WHERE u.id = :userId
    """, nativeQuery = true)
    List<Object[]> findUserDetailsWithProductsNatively(Long userId);
}
