const express = require("express");
const connectDB = require("./db");

const internshipRoutes = require("./routes/internship.routes");
const userRoutes = require("./routes/user.routes");
const matchRoutes = require("./routes/match.routes");

const app = express();
app.use(express.json());

connectDB();

app.use("/internships", internshipRoutes);
app.use("/users", userRoutes);
app.use("/match", matchRoutes);

app.listen(5000, () => console.log("🚀 Server running on port 5000"));
