package com.ue.roundworld.ui;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input.Keys;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.math.Rectangle;
import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.scenes.scene2d.actions.Actions;
import com.ue.roundworld.AssetManager;
import com.ue.roundworld.BaseActor;
import com.ue.roundworld.InputProcess;
import com.ue.roundworld.RoundWorld;
import com.ue.roundworld.Utils;
import com.ue.roundworld.client.Client;

public class UiBase extends BaseActor {

	private Bar phb;
	private Bar pmb;

	private Chat chat;

	private Vector2 mousePos = new Vector2();
	
	public ShapeRenderer shapeRenderer = new ShapeRenderer();

	public UiBase() {
		super(Utils.emptyTexture);

		// health bars
		phb = new Bar(AssetManager.getTexture("health_bar_back"), AssetManager.getTexture("health_bar_invert"), AssetManager.getTexture("health_bar"));
		pmb = new Bar(AssetManager.getTexture("mana_bar_back"), AssetManager.getTexture("mana_bar"), AssetManager.getTexture("mana_bar"));
		this.addActor(phb);
		this.addActor(pmb);
		pmb.sub(1);

		// chat
		chat = new Chat();
		this.addActor(chat);

		Gdx.input.setInputProcessor(chat.textInput);
		chat.addAction(Actions.fadeOut(0));
		
		resetElementPositions();
	}

	public void act(float dt) {
		super.act(dt);

		mousePos = this.screenToLocalCoordinates(new Vector2(Gdx.input.getX(), Gdx.input.getY()));

		//phb.sub(0.01f);
		
		if (Gdx.input.isKeyPressed(Keys.J)) {
			phb.sub(0.05f);
		}
		if (Gdx.input.isKeyPressed(Keys.H)) {
			phb.add(0.05f);
		}
		
		pmb.add(0.001f);
		chatUpdate();

	}

	/* moves UI elements back to initial positions based on RoundWorld.unscaledWidth and height */
	public void resetElementPositions()
	{
		phb.setPosition(0, RoundWorld.unscaledHeight - 16);
		pmb.setPosition(0, RoundWorld.unscaledHeight - (16 + 8));
		chat.setPosition(5, 5);
	}
	
	private void chatUpdate() {

		// use T to bring up chat
		if (Gdx.input.isKeyJustPressed(Keys.T)) {
			if (Gdx.input.getInputProcessor() == InputProcess.instance) {
				chat.addAction(Actions.fadeIn(1));
				Gdx.input.setInputProcessor(chat.textInput);
			}
		}

		// clicking outside unselects chat
		if (!chat.getBoundingRectangle().contains(mousePos) && Gdx.input.justTouched()
				|| Gdx.input.isKeyJustPressed(Keys.ESCAPE)) {
			Gdx.input.setInputProcessor(InputProcess.instance);
			chat.addAction(Actions.fadeOut(1));
			chat.textInput.erase();

		}

	}

	public void draw(Batch batch, float parentAlpha) {
		super.draw(batch, parentAlpha);
	}
}
