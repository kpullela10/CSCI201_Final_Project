// package com.usc.squirrelspotter.service;

// import org.springframework.beans.factory.annotation.Value;
// import org.springframework.stereotype.Service;
// import org.springframework.web.multipart.MultipartFile;

// import java.io.File;
// import java.io.IOException;
// import java.nio.file.Files;
// import java.nio.file.Path;
// import java.nio.file.Paths;
// import java.nio.file.StandardCopyOption;
// import java.util.UUID;

// /**
//  * Service for handling image uploads and storage
//  */
// @Service
// public class ImageStorageService {

//     @Value("${image.storage.path:./uploads/}")
//     private String storagePath;

//     /**
//      * Save uploaded image file and return the URL path
//      * @param file MultipartFile from request
//      * @return URL path to the saved image (relative to server)
//      * @throws IOException if file cannot be saved
//      */
//     public String saveImage(MultipartFile file) throws IOException {
//         if (file == null || file.isEmpty()) {
//             return null;
//         }

//         // Validate file type
//         String contentType = file.getContentType();
//         if (contentType == null || !contentType.startsWith("image/")) {
//             throw new IllegalArgumentException("File must be an image");
//         }

//         // Create uploads directory if it doesn't exist
//         Path uploadPath = Paths.get(storagePath);
//         if (!Files.exists(uploadPath)) {
//             Files.createDirectories(uploadPath);
//         }

//         // Generate unique filename
//         String originalFilename = file.getOriginalFilename();
//         String extension = "";
//         if (originalFilename != null && originalFilename.contains(".")) {
//             extension = originalFilename.substring(originalFilename.lastIndexOf("."));
//         }
//         String filename = UUID.randomUUID().toString() + extension;

//         // Save file
//         Path filePath = uploadPath.resolve(filename);
//         Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

//         // Return relative URL path
//         return "/uploads/" + filename;
//     }

//     /**
//      * Delete an image file
//      * @param imageUrl URL path to the image
//      */
//     public void deleteImage(String imageUrl) {
//         if (imageUrl == null || imageUrl.isEmpty()) {
//             return;
//         }

//         try {
//             // Extract filename from URL
//             String filename = imageUrl.substring(imageUrl.lastIndexOf("/") + 1);
//             Path filePath = Paths.get(storagePath, filename);
            
//             if (Files.exists(filePath)) {
//                 Files.delete(filePath);
//             }
//         } catch (IOException e) {
//             // Log error but don't throw - deletion failure is not critical
//             System.err.println("Failed to delete image: " + imageUrl);
//         }
//     }
// }

