import bpy
SETTINGS = "RENDER"

#コレクションの情報などの取得
ctx = bpy.context
scn = ctx.scene
objs = scn.objects
obj = objs.active
mesh = obj.data
dobjs = bpy.data.objects
dmeshes = bpy.data.meshes

#まだシェープキーがなければ、まず無意味だがとりあえずエラーでないように追加しよう
try:
    keys = mesh.shape_keys.key_blocks
    bss = keys[0]
except:
    bss = obj.shape_key_add(name = "Basis")
    keys = mesh.shape_keys.key_blocks

#元のシェープキー選択状態保存
askindex = obj.active_shape_key_index


#複製を作成する
#nobj = 目的のオブジェクト（モディファイアーが適用されたメッシュオブジェクト）
#nobj2 = 転送する為のメッシュ
objs0 = set(objs)
bpy.ops.object.duplicate_move()
nobj = tuple(set(objs) - objs0)[0]
nobj.name = "modified"

objs0 = set(objs)
bpy.ops.object.duplicate_move()
nobj2 = tuple(set(objs) - objs0)[0]


#多分、Basisで適用したいのでBasisを指定
nobj.active_shape_key_index = 0

#シェープキーを転送する為にオブジェクトの選択状態を調整する
for o in objs:
    o.select = False
nobj.select = True
objs.active = nobj
obj.select = False
nobj2.select = True

#モディファイアー適用する為に全シェープキー削除
bpy.ops.object.shape_key_remove(all=True)


#複製でのモディファイアー適用
for m in nobj.modifiers:
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier = m.name)
r = range(1,len(keys))
    
#新しいBasis追加
bss = nobj.shape_key_add(name = "Basis")
keys2 = nobj.data.shape_keys.key_blocks

#元オブジェクトのシェープキーを一つずつ:
#アクティブに指定>モディファイアーの適用>ダミーメッシュへのコピー>目的のメッシュへの転送
#を繰り返す
for kidx in r:
    print(kidx,keys[kidx])
    obj.active_shape_key_index = kidx
    nobj2.data = obj.to_mesh(scn,apply_modifiers = True,settings = SETTINGS)
    bpy.ops.object.join_shapes()
    keys2[-1].name = keys[kidx].name
    
#元々アクティブだったシェープキーを復元
obj.active_shape_key_index = askindex

#掃除
m = nobj2.data
objs.unlink(nobj2)
dobjs.remove(nobj2)
dmeshes.remove(m)