module.exports = {
    //base:'/en/docs/',
    cache:false,
    title: "",
    description: "My VuePress powered docs",
    themeConfig: {
        logo: '/logo.png',
        displayAllHeaders: false,
        nav: [
          { text: "SignUp", link: "https://app.jexia.com/signup" },
          { text: "Login", link: "https://app.jexia.com/login" }
        ],
        sidebar: [
            "/get-started/",
            "/auth/",
            "/dataset/",
            "/fileset/",
            "/ums/",
            "/pubsub/",  
            "/apphost/",
            "/automation/",
            "/integration/",
            "/cli/"   
        ]
    },
    plugins: [ 'code-switcher', '@vuepress/medium-zoom' ]
  };