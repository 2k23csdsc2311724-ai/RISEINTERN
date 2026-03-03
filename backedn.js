const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    await mongoose.connect("mongodb://localhost:27017/riseintern", {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log("✅ MongoDB Connected");
  } catch (error) {
    console.error("❌ DB Error:", error);
  }
};

module.exports = connectDB;
