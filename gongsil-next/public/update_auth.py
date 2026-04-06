import os
import re

file_path = r"c:\Users\user\Desktop\test\supabase_auth.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

replacement = """
window.handleLoginClick = async function(e) {
    if(e) e.preventDefault();
    try {
        let p = window.location.pathname;
        if(p !== "/" && !p.endsWith(".html") && !p.endsWith("/")) {
            p += ".html";
        }
        const url = window.location.origin + p + window.location.search;
        const { error } = await window.gongsiClient.auth.signInWithOAuth({
            provider: "google", 
            options: { redirectTo: url }
        });
        if(error) {
            console.error(error);
            alert("로그인 에러: " + error.message);
        }
    } catch(err) {
        console.error(err);
        alert("에러: " + err.message);
    }
};

loginBtns.forEach(btn => {
    btn.addEventListener("click", window.handleLoginClick);
});
"""

# Regex replacing the old loginBtn.forEach block
content = re.sub(r'loginBtns\.forEach\([^;]+?\}\);\n\}\);', replacement.strip(), content, flags=re.DOTALL)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Auth script updated.")
