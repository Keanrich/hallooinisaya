const app = Vue.createApp({
    data() {
        return {
            isSpecial: false,
            isUrgent:false,
            showMessage: true,
            Message: "Hello, IBDA 2023",

            notes:  [
                {
                    code: "N1",
                    remark: "catatan1",
                    isUrgent: false,
                },
                {
                    code: "N2",
                    remark: "catatan2",
                    isUrgent: true,
                },
                {
                    code: "N3",
                    remark: "catatan3",
                    isUrgent: false,
                }
            ]
        }
    },
    computed:{
        bigMessage () {
            return this.Message.toUpperCase()
        },
        notesCount () {
            return this.notes.length
        }
    },

    methods:{
        alwaysThree () {
            return 3
        },
        changeMessage () {
            this.Message = "Hello bro"
        },
        hideMessage () {
            this.showMessage= false
        },
        makeBigMessageSpecial () {
            this.isSpecial = true
        },
        restart () {
            this.Message = "Hello, IBDA 2023"
            this.showMessage = true
        }
    }
})

app.mount("#app")