require("dotenv").config();
const { IgApiClient } = require('instagram-private-api');
const { get } = require('request-promise');

const postToInstaStory = async () => {
    const ig = new IgApiClient();
    ig.state.generateDevice(process.env.IG_USERNAME);
    await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);

    const imageBuffer = await get({
        url: 'https://i.imgur.com/BZBHsauh.jpg',
        encoding: null,
    });

    // Get user ID for the mention
    const userToMention = await ig.user.searchExact('statbuy.co');

    await ig.publish.story({
        file: imageBuffer,
        story_sticker_ids: [
            {
                user_id: userToMention.pk,
                x: 0.5,  // Positioning x (0 to 1)
                y: 0.5,  // Positioning y (0 to 1)
                width: 0.5, // Width of the sticker (0 to 1)
                height: 0.1, // Height of the sticker (0 to 1)
                rotation: 0, // Rotation of the sticker
            },
        ],
    });

    console.log('Story posted with mention!');
};

postToInstaStory();
