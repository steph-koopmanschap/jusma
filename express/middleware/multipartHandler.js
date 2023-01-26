const busboy = require("busboy");
const { v4: uuidv4 } = require("uuid");
const appendField = require("append-field");
const fs = require("fs");

function logFileInfo(info) {
    console.log("all file info", info);
    const { filename, encoding, mimeType } = info;
    console.log(`File []: filename: %j, encoding: %j, mimeType: %j`, filename, encoding, mimeType);
}

const getFileExtension = (info) => info.mimeType.match(/(?<=\/).+/)[0];
const isImage = (mimeType) => ["image/gif", "image/jpeg", "image/jpg", "image/png"].includes(mimeType);
const isVideo = (mimeType) => [].includes(mimeType);
const isAudio = (mimeType) => [].includes(mimeType);

function determineSaveTo(formData, entry_id, fileExtension) {
    const { context, isPrivate } = formData;
    let saveTo = "./media";
    if (context === "post") {
        saveTo += `/posts/${entry_id}.${fileExtension}`;
    }

    if (context === "comment") {
        saveTo += `/comments/${entry_id}.${fileExtension}`;
    }

    if (context === "avatar") {
        saveTo += `/avatars/${entry_id}.${fileExtension}`;
    }
    return saveTo;
}

const contextExists = (formData) => formData?.context;
const isValidContext = (formData) => ["avatar", "post", "comment"].includes(formData.context);

function formatVal(val) {
    if (val === "true") {
        return true;
    }

    if (val === "false") {
        return false;
    }

    return val;
}

async function multipartHandler(req, res, next) {
    try {
        const bb = busboy({ headers: req.headers });
        const formData = Object.create(null);
        formData.assignedEntryId = uuidv4();
        let fileExists = false;
        let textExists = false;

        bb.on("field", (name, val, info) => {
            appendField(formData, name, formatVal(val));
        }).on("close", () => {
            console.log("formdata on close", formData);
            if (formData.text) {
                textExists = true;
            }
        });

        bb.on("file", (name, file, info) => {
            fileExists = true;
            const fileExtension = getFileExtension(info);
            const saveTo = determineSaveTo(formData, assignedEntryId, fileExtension);
            file.pipe(fs.createWriteStream(saveTo));
        });

        bb.on("close", () => {
            if (!textExists && !fileExists) {
                return res.json({ success: false, message: "Post must include content" });
            }

            if (!contextExists(formData)) {
                return res.json({
                    success: false,
                    message: "Context must be provided in form data. Available contexts are [avatar, comment, post]"
                });
            }

            if (!isValidContext(formData)) {
                return res.json({
                    success: false,
                    message: "Not a valid context. Available contexts are [avatar, comment, post]"
                });
            }

            req.body = formData;
            next();
        });

        req.pipe(bb);
    } catch (error) {
        console.log(error);
    }
}

module.exports = { multipartHandler };