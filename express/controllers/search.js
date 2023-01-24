const db = require("../db/connections/jasmaAdmin");
const { User, Post, Comment, PostHashtag } = db.models;

async function searchHashtags(keyword) {
    keyword = `%${keyword}%`;
    console.log("keyword:");
    console.log(keyword);
    // I DONT KNOW WHY THIS DOESNT WORK!!
    /*
        jasma/express/node_modules/sequelize/lib/utils/sql.js:150
        throw new Error(`Positional replacement (?) ${replacementIndex} has no entry in the replacement map (replacements[${replacementIndex}] is undefined).`);
        Error: Positional replacement (?) 0 has no entry in the replacement map (replacements[0] is undefined).
    */
    const resHashtags = await db.query(`SELECT * FROM posts_hashtags WHERE LOWER(hashtag) LIKE ?`, { replacements: [keyword] });
    const posts = [];

    //Retrieve posts accociated with each hashtag
    for (let i = 0; i < resHashtags[0].length; i++)
    {
        const user_id = resHashtags[0][i].user_id;
        const resPost = await db.query(`SELECT * FROM posts WHERE user_id = ?`, { replacements: [user_id] });
        posts.push(resPost[0][0]);
    }

    return posts; 
}    

/*
    NOTE:
    https://stackoverflow.com/questions/7005302/how-to-make-case-insensitive-query-in-postgresql
*/

async function searchPosts(keyword) {
    keyword = `%${keyword}%`;
    const resPosts = await db.query(`SELECT * FROM posts WHERE LOWER(text_content) LIKE ?`, { replacements: [keyword] });

    return resPosts[0];
}

async function searchComments(keyword) {
    keyword = `%${keyword}%`;
    const resComments = await db.query(`SELECT * FROM comments WHERE LOWER(comment_text) LIKE ?`, { replacements: [keyword] });

    return resComments[0];
}    

async function searchUsers(keyword) {
    keyword = `%${keyword}%`;
    const resUsers = await db.query(`SELECT user_id, username FROM users WHERE LOWER(username) LIKE ?`, { replacements: [keyword] });

    return resUsers[0];
}

async function search(req, res) {
    const { q, filter } = req.query;
    //Make the search keyword lower case so the search becomes case insensitive
    let keyword = q.toLowerCase(); 
    let result = "";

    //Prevent server crash if keyword is undefined
    if (!keyword || keyword === "") {
        return res.json({ success: false, message: `Nothing found.` });
    }

    //Filter which kind of specific search we need.
    switch (filter)
    {
        
        case "hashtags":
            result = await searchHashtags(keyword);
            break;
    
        case "posts":
            result = await searchPosts(keyword);
            break;
        
        case "comments":
            result = await searchComments(keyword);
            break;
        
        case "users":
            result = await searchUsers(keyword);
            break;
        
        default:
            break;       
    }

    if (result === "" || result === null || result?.length === 0)
    {
        return res.json({ success: false, message: `Search for ${q} gave no results. Nothing found.` });
    }
    return res.json({ success: true, result: result });
}

module.exports = {
    search
};
