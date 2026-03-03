const Internship = require("../models/internship.model");

exports.getAll = async (req, res) => {
  const data = await Internship.find().sort({ scraped_at: -1 });
  res.json(data);
};

exports.addOrUpdate = async (req, res) => {
  try {
    const job = req.body;

    await Internship.updateOne(
      {
        title: job.title,
        company: job.company,
        apply_link: job.apply_link,
      },
      { $set: job },
      { upsert: true }
    );

    res.json({ message: "Saved successfully" });
  } catch (err) {
    res.status(500).json({ error: err });
  }
};
