module.exports = {
    //base:'/en/docs/',
    cache:false,
    title:"Jexia documentation",
    dest:"./dist",
    description: "Make development easier",
    themeConfig: {
        logo: '/logo.jpg',
        smoothScroll: true,
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