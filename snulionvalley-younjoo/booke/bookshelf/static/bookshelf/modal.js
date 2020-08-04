$( document ).ready(function() {
});

$('#signup-form').submit((event) => {
    event.preventDefault()
    $.ajax({
        url: '/accounts/signup/',
        method: 'POST',
        dataType: 'json',
        data: {
            csrfmiddlewaretoken: $(event.currentTarget).data('csrfmiddlewaretoken'),
            username: $(`input#username`).val(),
            password1: $(`input#password1`).val(),
            password2: $(`input#password2`).val(),
            goal: $(`#goal option:selected`).val(),
            taste: $(`#taste option:selected`).val(),
        },
        success(response) {
            console.log(response)
            window.location.href='/bookshelf/'
        },
        error(response, status, error) {
            console.log(response, status, error);
        }
    })

    
})

$('#login-form').submit((event) => {
    event.preventDefault()
    $.ajax({
        url: '/accounts/login/',
        method: 'POST',
        data: {
            login: $(`input#login-username`).val(),
            password: $(`input#password`).val(),
            csrfmiddlewaretoken: $(event.currentTarget).data('csrfmiddlewaretoken')
        },
        dataType: "json",
        success(res) {
            console.log(res)
            window.location.href='/bookshelf/'
        },
        error(response, status, error) {
            console.log(response, status, error);
        }
    })
})

$('#book-create').submit((event) => {
    event.preventDefault()
    var colors = document.getElementsByName('color');
        var color_value;
        for(var i = 0; i < colors.length; i++){
            if(colors[i].checked){
                color_value = colors[i].value;
                // console.log(color_value)
            }
            // return color_value;
        }

    $.ajax({
        url: '/bookshelf/',
        method: 'POST',
        data: {
            title: $(`input#title`).val(),
            // author: $(`input#author`).val(),
            // page: $(`input#page`).val(),
            author: $(`input#author`).val(),
            color: color_value,
            csrfmiddlewaretoken: $(event.currentTarget).data('csrfmiddlewaretoken')
        },
        dataType: "json",
        success(res) {
            console.log(res);
            window.location.href='/bookshelf/'
        },
        error(response, status, error) {
            console.log(response, status, error);
        }
    })
    // .then(res => {
       
    //     var colors = document.getElementsByName('color');
    //     var color_value;
    //     for(var i = 0; i < colors.length; i++){
    //         if(colors[i].checked){
    //             color_value = colors[i].value;
    //             // console.log(color_value)
    //         }
    //         // return color_value;
    //     }
    //     console.log(color_value);
    //     console.log(`${res.id}`);
    //     console.log($(`#${res.id}`));
    //     // document.getElementById(`${res.id}`).classList.add(`btn-${color_value}`);
    //     $(`#${res.id}`).addClass(`book-${color_value}`);
    // })         
})

$('.showmodal').click((e) => {
    e.preventDefault();
    const $this = $(e.currentTarget);
    const id = $this.data('id');
    const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');

    $.ajax({
        type: 'GET',

        url: `/bookshelf/${id}`, 
        data: { 
            id: id,
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            //content: $(`input#${id}[name=content]`).val(),
        },
        dataType: "json",
        success(res) {
            console.log(res)
            //window.location.href=`/bookshelf/${id}/`
        },
        error(response, status, error) {
            console.log(response, status, error);
        }

    }).then((data) => {
        const userbook = data.userbook;
        const memos = data.memos;
        /*let $title = document.getElementById('userbook.bookid.title');
        $($title).find('p').remove();
        const userbookTitle = `<p>책 제목 : ${userbook.title}</p>`;
        $(userbookTitle).prependTo($title);
        let $author = document.getElementById('userbook.bookid.author.name');
        $($author).find('p').remove();
        const userbookAuthor = `<p>작가 : ${userbook.author}</p>`;
        $(userbookAuthor).prependTo($author);*/

        let info_div=document.getElementById('info-div')
        let memo_div=document.getElementById('memo-div');
        let str=``
        console.log(memos.length);

        for (let i=0; i<memos.length; i++){
            console.log(`${memos.i.page}`);
            console.log(`${memos.i.created_at}`);
            console.log(`${memos.i.content}`);

            str+=`<p> ${memos.i.page}, ${memos.i.created_at},${memos.i.content}</p>`;
        }
        console.log(str);
        info_div.innerHTML=`<p>책 제목 : ${userbook.title}</p>
        <p>작가 : ${userbook.author}</p>`;
        memo_div.innerHTML=`<div>지난 감상</div><div>${str}</div>`;
        
        document.getElementById('submit-memo').setAttribute('data-id', `${id}`); 
        
        // const tempalte = memos.map(
        //     memo => xxxtemplate(memo)
        // ).join(".")

        // const xx .inneh = tempalte;

    })
})


$('#submit-memo').click( (e) => {
    e.preventDefault()
    const $this = $(e.currentTarget);
    const id = $this.data('id');
    console.log(id);
    // 보통 이벤트가 일어난 객체의 id를 가져오는데 이건 책장에서 책등의 id를 가져오는 게 아니라 
    // modal form의 id를 가져오게 될텐데,, 지금 확인이 안 되지만 일단 이렇게 써둘게요
    const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');

    $.ajax({
        url: `/bookshelf/${id}/memos/`,         
        method: 'POST',
        data: {
            id:id,
            content: $(`textarea#review`).val(),
            page: $(`input#review_pages`).val(),
            csrfmiddlewaretoken: csrfmiddlewaretoken,
        },
        dataType: "json",
        success(res) {
            console.log(res)
            //window.location.href=`/bookshelf/${id}/`
        },
        error(response, status, error) {
            console.log(response, status, error);
        }
    }).then((data) => {
        const userbook = data.userbook;
        const memos = data.memos;
        /*let $title = document.getElementById('userbook.bookid.title');
        $($title).find('p').remove();
        const userbookTitle = `<p>책 제목 : ${userbook.title}</p>`;
        $(userbookTitle).prependTo($title);
        let $author = document.getElementById('userbook.bookid.author.name');
        $($author).find('p').remove();
        const userbookAuthor = `<p>작가 : ${userbook.author}</p>`;
        $(userbookAuthor).prependTo($author);*/
        let info_div=document.getElementById('info-div')
        info_div.innerHTML=`<p>책 제목 : ${userbook.title}</p>
        <p>작가 : ${userbook.author}</p>`;
        let memo_div=document.getElementById('memo-div');
        let str=``
        console.log(memos.length);
        for (let i=0; i<memos.length; i++){
            str+=`<p> ${memos.i.page}, ${memos.i.created_at},${memos.i.content}</p>`;

        }
        console.log(str);
        memo_div.innerHTML=`<div>지난 감상</div><div>${str}</div>`
    })
})


$(document).ready(() => {
    $(".more-comment-btn").on('click', function(event) {
        $(this).toggleClass("showing-comment");
    
        if ($(this).hasClass("showing-comment")) {
            $(this).text("HIDE COMMENTS");
            $(this).parent().find(".toggle-comment").not(".last-comment").show();
        } else {
            $(this).text("MORE COMMENTS");
            $(this).parent().find(".toggle-comment").not(".last-comment").hide();
        }
    });
}
)