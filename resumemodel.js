const mongoose = require("mongoose");

const ResumeSchema = new mongoose.Schema(
  {
    user_id: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    skills: [String],
    projects: [String],
    education: String,
    experience: String,
  },
  { timestamps: true }
);

module.exports = mongoose.model("Resume", ResumeSchema);
