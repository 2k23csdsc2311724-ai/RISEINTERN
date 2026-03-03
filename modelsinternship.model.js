const mongoose = require("mongoose");

const InternshipSchema = new mongoose.Schema(
  {
    title: String,
    promo: String,
    tagline: String,
    company: String,
    location: String,
    stipend: String,
    duration: String,
    skills: [String],
    posted: String,
    apply_link: { type: String, required: true },
    platform: String,
    scraped_at: { type: Date, default: Date.now }
  },
  { timestamps: true }
);

InternshipSchema.index({ title: 1, company: 1, apply_link: 1 }, { unique: true });

module.exports = mongoose.model("Internship", InternshipSchema);
