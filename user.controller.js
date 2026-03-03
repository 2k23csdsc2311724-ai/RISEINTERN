const User = require("../models/user.model");

exports.register = async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.json({ message: "User registered", user });
  } catch (err) {
    res.status(400).json({ error: "Email already exists" });
  }
};

exports.login = async (req, res) => {
  const user = await User.findOne({ email: req.body.email });

  if (!user || user.password !== req.body.password)
    return res.status(400).json({ error: "Invalid credentials" });

  res.json({ message: "Login success", user });
};
