import { getSubscribedHashtags, subscribeToHashtags, unsubscribeFromHashtag } from "@/entities/hashtags";
import { useQuery } from "react-query";

/**
 *
 * @param {String} hashtag hashtag in string format
 * @returns
 */

const handleUnsubscribeHashtag = async (hashtag) => {
    try {
        const res = await unsubscribeFromHashtag(hashtag);
        return res;
    } catch (error) {
        return { error: true, message: "Error." + error };
    }
};

/**
 *
 * @param {String} hastags hashtags in string format
 * @returns
 */

const handleSubToHashtags = async (hastags) => {
    try {
        const res = await subscribeToHashtags(hastags);
        return res;
    } catch (error) {
        return { error: true, message: "Error." + error };
    }
};

const useGetHastags = () => {
    return useQuery(
        [`subscribedHashtags`],
        async () => {
            return await getSubscribedHashtags();
        },
        {
            enabled: true,
            refetchOnWindowFocus: false
        }
    );
};

export { handleUnsubscribeHashtag, handleSubToHashtags, useGetHastags };
