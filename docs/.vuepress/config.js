module.exports = {
    //base:'/en/docs/',
    head: [ ['script', {}, ` 
        (function(h,o,t,j,a,r){
          h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
          h._hjSettings={hjid:1675007,hjsv:6};
          a=o.getElementsByTagName('head')[0];
          r=o.createElement('script');r.async=1;
          r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
          a.appendChild(r);
      })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
    `]],
    cache:false,
    title:"Jexia documentation",
    dest:"./dist",
    description: "Make development easier",
    themeConfig: {
        logo: '/logo-decorated.svg',
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
    plugins: [ 'code-switcher', '@vuepress/medium-zoom', 
          [
            'vuepress-plugin-google-tag-manager',
            {
              'gtm': 'GTM-MNDDVVW' // UA-00000000-0
            }
          ]
    ]
  };