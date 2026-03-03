const router = require("express").Router();
const controller = require("../controllers/match.controller");

router.post("/resume", controller.saveResume);
router.get("/match", controller.matchInternships);

module.exports = router;
