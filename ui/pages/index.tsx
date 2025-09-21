import React, {useState} from 'react'

export default function Home(){
  const [q,setQ] = useState('What is GHGold?')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const backend = process.env.NEXT_PUBLIC_BACKEND_URL || ''

  async function ask(){
    const url = (backend ? backend : '') + '/ask'
    try{
      const res = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({q:q, top_k:4})})
      const data = await res.json()
      setAnswer(data.answer || JSON.stringify(data))
      setSources(data.sources || [])
    }catch(e){
      setAnswer('Error: '+String(e))
    }
  }

  return (
    <div style={{maxWidth:900, margin:'40px auto', fontFamily:'system-ui'}}>
      <h1>Anaasɛ Portal</h1>
      <textarea style={{width:'100%',height:140}} value={q} onChange={e=>setQ(e.target.value)}/>
      <div style={{marginTop:8}}><button onClick={ask}>Ask Anaasɛ</button></div>
      <h3>Answer</h3>
      <pre style={{whiteSpace:'pre-wrap'}}>{answer}</pre>
      <h4>Sources</h4>
      <pre style={{whiteSpace:'pre-wrap'}}>{sources.join('\n')}</pre>
    </div>
  )
}
