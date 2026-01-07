// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ProductVerification {
    struct Product {
        string cid;        // IPFS content ID (points to product data/images)
        string issuer;     // Manufacturer or brand
        uint256 timestamp; // Block timestamp when registered
        bool exists;       // Flag to check if registered
    }

    mapping(string => Product) private products;

    event ProductRegistered(
        string productId,
        string cid,
        string issuer,
        uint256 timestamp
    );

    /// @notice Register a new product with productId, IPFS CID, and issuer
    /// @param productId Unique product identifier (e.g., QR code string)
    /// @param cid IPFS content identifier of product details
    /// @param issuer Manufacturer/brand name
    function registerProduct(
        string memory productId,
        string memory cid,
        string memory issuer
    ) public {
        require(!products[productId].exists, "Product already registered");
        products[productId] = Product(cid, issuer, block.timestamp, true);
        emit ProductRegistered(productId, cid, issuer, block.timestamp);
    }

    /// @notice Fetch details of a registered product
    /// @param productId Unique product identifier
    /// @return cid IPFS CID
    /// @return issuer Manufacturer/brand
    /// @return timestamp Registration time
    /// @return exists Whether product exists
    function getProduct(string memory productId)
        public
        view
        returns (string memory cid, string memory issuer, uint256 timestamp, bool exists)
    {
        Product memory p = products[productId];
        return (p.cid, p.issuer, p.timestamp, p.exists);
    }

    /// @notice Verify if a product exists
    /// @param productId Unique product identifier
    /// @return bool True if registered
    function verifyProduct(string memory productId) public view returns (bool) {
        return products[productId].exists;
    }
}
