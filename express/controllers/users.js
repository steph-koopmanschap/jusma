const db = require("../db/connections/jasmaAdmin");
const { User, UserInfo } = db.models;
const fs = require("fs");

async function getUserIdByUsername(req, res) {
    const { username } = req.params;
    let result = null;
    let userID = "";
    try {
        result = await User.getByUsername(username);
        userID = result.user_id;
    } catch (e) {
        return res.json({ success: false, message: `User ${username} not found.` });
    }

    return res.json({ success: true, user_id: userID });
}

async function getClientUser(req, res) {
    const { user_id } = req.session;
    const user = await User.getById(user_id);
    return res.json({ user });
}
async function getUserInfo(req, res) {
    const { userID } = req.params;
    console.log("HELLO 0 FROM getUserInfo uers.js controller");
    let resUserInfo = null;
    let resUser = null;
    try {
        console.log("HELLO 1!");
        resUserInfo = await UserInfo.getById(userID);
        resUser = await User.getById(userID);
        console.log("HELLO 2!");
    } catch (e) {
        console.log(e);
        return res.json({ success: false, message: `User info not found.` });
    }

    console.log("HELLO 3!");

    const returnData = {
        given_name: resUserInfo.given_name,
        last_name: resUserInfo.last_name,
        bio: resUserInfo.bio,
        date_of_birth: resUserInfo.date_of_birth,
        country: resUserInfo.country,
        city: resUserInfo.city,
        website: resUserInfo.website,
        email: resUser.email,
        phone: resUser.phone
    };

    return res.json({ success: true, userInfo: returnData });
}

async function getProfilePic(req, res) {
    const { userid } = req.params;
    const options = {
        root: appRoot
    };
    //If userid is undefined postgresql will give an error and crash the server.
    //This if-block prevents the server from crashing and sends the default profile pic
    if (userid === "undefined" || userid === undefined || userid === false || userid === "null" || userid === null) {
        res.sendFile("/media/users/00000000-0000-0000-0000-000000000000/profile-pic.webp", options, (err) => {
            if (err) {
                res.json({ success: false, message: "File not found." });
            }
        });
        return 1;
    }
    const fileUrlObj = await UserInfo.getProfilePicUrl(userid);
    const fileUrl = fileUrlObj.profile_pic_url;

    res.sendFile(fileUrl, options, (err) => {
        if (err) {
            res.json({ success: false, message: "File not found." });
        }
    });
}

// // Alternative getProfilePic function. (DOES NOT WORK)
// async function getProfilePic(req, res) {
//     const { userid } = req.params;
//     //Send the default profile pic unknown userid
//     if (userid === 'undefined' || userid === undefined || userid === false || userid === 'null' || userid === null) {
//         return res.json({ success: false, file_url: "/media/users/00000000-0000-0000-0000-000000000000/profile-pic.webp" });
//     }
//     //Check if the file exists, if not revert back to the default user id.
//     fs.open(`/media/users/${userid}/profile-pic.webp`, 'r', (err, fd) => {
//         console.log("HELLO!");
//         return res.json({ success: false, file_url: "/media/users/00000000-0000-0000-0000-000000000000/profile-pic.webp" });
//     });

//     return res.json({ success: true, file_url: `/media/users/${userid}/profile-pic.webp` });
// }

module.exports = {
    getUserIdByUsername,
    getUserInfo,
    getProfilePic,
    getClientUser
};
